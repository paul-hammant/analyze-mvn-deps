#!/usr/bin/env python3

import os
import subprocess
import re
import requests
from natsort import natsorted
import shutil


def highest_upgrade_for(version_now, available_versions):
    if len(available_versions) == 0:
        return ""
    normalized_available_versions = []
    for ver_avail in available_versions:
        ver_avail = ver_avail.lower()

        matches = re.search("(\d)([a-z])", ver_avail)
        if matches:
            ver_avail = ver_avail.replace(matches.group(1)+matches.group(2),
                                          matches.group(1)+ "-" + matches.group(2))
        if "beta" not in ver_avail and "alpha" not in ver_avail \
                and "rc" not in ver_avail and "m" not in ver_avail:
            ver_avail = ver_avail + "-zzz"
        normalized_available_versions.append(ver_avail)

    sorted_versions = natsorted(normalized_available_versions, key=lambda x: x.replace('.', '~')+'z', reverse=True)
    highest = available_versions[normalized_available_versions.index(sorted_versions[0])]
    if highest == version_now:
        return ""

    return highest


def recommended_version_upgrades(version_now, available_versions):

    upg = highest_upgrade_for(version_now, available_versions)

    if upg == version_now:
        return ""

    # Look for point revision upgrades
    munged_version = version_now
    while len(munged_version) > 0:
        subset_list = []
        for ver_avail in available_versions:
            if ver_avail.startswith(munged_version):
                subset_list.append(ver_avail)
        if len(subset_list) > 0:
            another_possible_upgrade = highest_upgrade_for(munged_version, subset_list)
            if another_possible_upgrade != "" and another_possible_upgrade != version_now and another_possible_upgrade not in upg:
                upg =  upg + ", " + another_possible_upgrade
        munged_version = ".".join(munged_version.split(".")[:-1])

    return ", ".join(sorted(upg.split(", "), reverse=True))


misleading_gavs = """
commons-beanutils:commons-beanutils:dev
commons-beanutils:commons-beanutils:200
commons-io:commons-io:200
commons-lang:commons-lang:2003
com.google.guava:guava:r0
"""

misleading_gav_list = misleading_gavs.split("\n")

def misleading(group, artifact, version):
    gav = ":".join([group, artifact, version])
    for misleading_gav in misleading_gav_list:
        if misleading_gav is not "" and misleading_gav in gav:
            return True
    return False

if __name__ == "__main__":

    if os.path.isfile(".deps") or os.path.isdir(".deps"):
        shutil.rmtree(".deps")

    os.mkdir(".deps")


def parse_dependencies_from_maven_output():
    with open(".deps/mvn-dep-tree-output.txt", "w") as mvn_dep_tree_output:
        for line in rawoutput:
            if "[INFO]" in line or "[WARNING]" in line:  # if not ("Downloading" in line or "Downloaded" in line or "Progress" in line):
                mvn_dep_tree_output.write(line)
                mvn_dep_tree_output.write('\n')
                output.append(line)
            if "Total time" in line:
                break


def write_to_text_dependencies_tree_output():
    dependency_tree = []
    with open(".deps/dependencies-tree.txt", "w") as f:
        for line in output:
            if "Reactor Summary:" in line:
                break
            s = line.replace("|", " ").replace("+-", "  ").replace("\\-", "  ").replace("[INFO]", "")
            if "---" not in s and "--<" not in s and not s.startswith(" Building ") and not s.endswith("[jar]") and not s.endswith("[pom]"):
                if re.search(":", s) is not None:
                    if re.search(":$", s) is None:
                        if not "Total time" in s and not "[WARNING]" in s:
                            s = s.replace("   ", " ")
                            s = re.sub("^ ", "", s)
                            if not "::" in s:
                                s = re.sub("maven-dependency-plugin:[0-9\.]*:tree \(default-cli\) @ ", "", s)
                                f.write(s)
                                f.write("\n")
                                dependency_tree.append(s)
    return dependency_tree


def determine_list_of_versions():
    list_of_versions = []
    r = requests.get("http://central.maven.org/maven2/" + groupDir + "/" + artifact)
    req_lines = r.text.split("\n")
    req_lines = list(map(lambda x: re.sub("\-         \-", "unknown-date unknown:time", x), req_lines))
    req_lines = list(map(lambda x: re.sub("\W+-\W+$", "", x), req_lines))
    req_lines = list(filter(lambda x: "href" in x and not "maven-metadata" in x and not ">../</" in x, req_lines))
    for line2 in req_lines:
        p = re.findall(".*>(.*)/</a>(.*)", line2)
        if len(p) == 0:
            continue
        p = list(p[0])
        p = list(map(lambda x: x.strip(), p))
        p = p[0]
        if not misleading(group, artifact, p):
            list_of_versions.append(p)
    return list_of_versions


if __name__ == "__main__":

    if os.path.isfile(".deps") or os.path.isdir(".deps"):
        shutil.rmtree(".deps")

    os.mkdir(".deps")

    print("Getting dependency tree for current directory")

    try:
        rawoutput = subprocess.check_output(["mvn", "dependency:tree"]).decode('utf-8').split('\n')
        output = []
    except subprocess.SubprocessError as e:
        print("Some problems occured with: ", e.cmd)
        print("Return code: ", e.returncode)
        with open("error.log", "w") as errorFile:
            errorFile.write(e.output.decode("utf-8"))
            print("Check error.log for details")
        exit(1)

    parse_dependencies_from_maven_output()

    dependency_tree = write_to_text_dependencies_tree_output()

    flattened_unique_gavs = [":".join(s.replace(" ", "").split(":")[:4]) for s in dependency_tree if ":" in s and re.search("-+<.*>-+", s) is None]
    flattened_unique_gavs = sorted(list(set(flattened_unique_gavs)))

    with open(".deps/flattened-unique-gavs.txt", "w") as f:
        f.write("\n".join(flattened_unique_gavs))

    for line in flattened_unique_gavs:
        group, artifact, typ, version = line.split(":")
        groupDir = group.replace(".", "/")
        list_of_versions = []
        try:
            list_of_versions = determine_list_of_versions()
        except requests.exceptions.RequestException:
            print("Connection problems for GAV:", ":".join([group, artifact, typ, version]))
            continue
        list_of_versions = (recommended_version_upgrades(version, list_of_versions)).split(", ")
        list_of_versions_with_current = list_of_versions
        current_index = None
        for i in range(len(list_of_versions_with_current)):
            if list_of_versions_with_current[i] == version:
                list_of_versions_with_current[i] = version + " ***"
                current_index = i
        if current_index is not None:
            list_of_versions_since_current = list_of_versions_with_current[:current_index+1]
        else:
            list_of_versions_since_current = list_of_versions_with_current
        if len(list_of_versions_since_current) > 0:
            prospectiveVersion= ", ".join(list_of_versions_since_current)
            if list_of_versions_since_current[0] != version and prospectiveVersion != "":

                regex = "(.* "+group+":"+artifact+":[^ ]*)$"
                with open(".deps/dependencies-tree.txt", "w") as f:
                    for i in range(len(dependency_tree)):
                        if re.search(regex, dependency_tree[i]) is not None:
                            dependency_tree[i] = dependency_tree[i] + "  > " +str(prospectiveVersion)
                        f.write(dependency_tree[i])
                        f.write("\n")

    with open(".deps/immediate-upgrade-opportunities.txt", "w") as f:
        f.write("\n".join(list(sorted(set([d for d in dependency_tree if re.search("^  ", d) is None and re.search(">", d) is not None])))))

    print("Check the .deps/ directory")
