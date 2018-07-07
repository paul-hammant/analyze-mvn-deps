#!/usr/bin/env python3

import os
import sys
import subprocess
import re
import requests
from natsort import natsorted
import shutil


def recommended_version_upgrades(version_now, available_versions_str):
    availavle_versions = available_versions_str.split(", ")
    normalized_available_versions = []
    for ver_avail in availavle_versions:
        ver_avail = ver_avail.lower()

        matches = re.search("(\d)([a-z])", ver_avail)
        if matches:
            ver_avail = ver_avail.replace(matches.group(1)+matches.group(2),
                                          matches.group(1)+ "-" + matches.group(2))
        if "beta" not in ver_avail and "alpha" not in ver_avail \
                and "rc" not in ver_avail and "m" not in ver_avail:
            ver_avail = ver_avail + "-zzz"
        normalized_available_versions.append(ver_avail)

    sorted_versions = sorted(normalized_available_versions, reverse=True)

    return availavle_versions[normalized_available_versions.index(sorted_versions[0])]


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

    with open(".deps/mvn-dep-tree-output.txt", "w") as mvn_dep_tree_output:
        for l in rawoutput:
            if "[INFO]" in l or "[WARNING]" in l: #if not ("Downloading" in l or "Downloaded" in l or "Progress" in l):
                mvn_dep_tree_output.write(l)
                mvn_dep_tree_output.write('\n')
                output.append(l)
            if "Total time" in l:
                break

    #print("Dependency tree for current directory acquired")
    #print("\n".join(rawoutput))
    #input("Raw Output, press Enter")

    dependency_tree = []

    with open(".deps/dependencies-tree.txt", "w") as f:
        for l in output:
            s = l.replace("|", " ").replace("+-", "  ").replace("\\-", "  ").replace("[INFO]", "")
            if re.search("^---", s) is None:
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

    #print("\n".join(dependency_tree))
    #input("Dependency tree, press Enter")

    flattened_unique_gavs = [":".join(s.replace(" ", "").split(":")[:4]) for s in dependency_tree if ":" in s and re.search("-+<.*>-+", s) is None]
    flattened_unique_gavs = sorted(list(set(flattened_unique_gavs)))

    with open(".deps/flattened-unique-gavs.txt", "w") as f:
        f.write("\n".join(flattened_unique_gavs))
        #print("\n".join(flattened_unique_gavs))
        #input("Flattened unique gavs, press Enter")

    #do_input = False
    for l in flattened_unique_gavs:
        #if l == 'com.esotericsoftware:minlog:jar:1.3.0':
            #do_input = True
        group, artifact, typ, version = l.split(":")
        #print(l.split(":"))
        groupDir = group.replace(".", "/")
        try:
            r = requests.get("http://central.maven.org/maven2/"+ groupDir + "/" + artifact)
        except requests.exceptions.RequestException:
            print("Connection troubles for package:", l)
            continue
        req_lines = r.text.split("\n")
        #print("\n".join(req_lines))
        req_lines = list(map(lambda x: re.sub("\-         \-", "unknown-date unknown:time", x), req_lines))
        #print("Put unknowns")
        #print("\n".join(req_lines))
        req_lines = list(map(lambda x: re.sub("\W+-\W+$", "", x), req_lines))
        #print("strip ends")
        #print("\n".join(req_lines))
        req_lines = list(filter(lambda x: "href" in x and not "maven-metadata" in x and not ">../</" in x, req_lines))
        #print("grep references")
        #print("\n".join(req_lines))
        #req_lines = list(filter(lambda x: re.search("beta", x, re.I) is None and re.search("alpha", x, re.I) is None and re.search("[Rr][Cc][\.]*[0-9]* ", x) is None, req_lines))
        #print("remove beta's and alphas")
        #print("\n".join(req_lines))
        list_of_versions = []
        #print("List of versions:")
        for l in req_lines:
            p = re.findall(".*>(.*)/</a>(.*)", l)
            #print(p)
            if len(p) == 0:
                continue
            p = list(p[0])
            p = list(map(lambda x: x.strip(), p))
            list_of_versions.append(p)
        #print(list_of_versions)
        list_of_versions = natsorted(list_of_versions, key=lambda x: x[0], reverse=True)
        #list_of_versions.sort(reverse=True, key=lambda x: LooseVersion(x[0]))
        #print("List of versions sorted: ")
        #print(list_of_versions)
        list_of_versions_with_current = list_of_versions
        current_index = None
        for i in range(len(list_of_versions_with_current)):
            if list_of_versions_with_current[i][0] == version:
                list_of_versions_with_current[i][0] = version + " ***"
                current_index = i
        #print("List of versions with current: ")
        #print(list_of_versions_with_current)
        if current_index is not None:
            list_of_versions_since_current = list_of_versions_with_current[:current_index+1]
        else:
            list_of_versions_since_current = list_of_versions_with_current
        #print("\n".join(list(map(lambda x: " ".join(x), list_of_versions_since_current))))
        with open(".deps/big-dependency-report.txt", "a") as f:
            f.write("\n========================================================================\nPresently in use: "+group+":"+artifact+"  "+ version+ "\n")
            #print("\n========================================================================\nPresently in use: "+group+":"+artifact+"  "+ version+ "\n")
            matches=[s for s in dependency_tree if re.search(group+":"+artifact, s)]
            if len(matches) == 0:
                continue
            leastTransitiveDep = sorted(matches)[-1]
            leastTransitiveDep = len(leastTransitiveDep) - len(leastTransitiveDep.strip())
            f.write("   - a level "+ str(leastTransitiveDep) + " dependencies among "+str(len(matches))+" (possibly transitive) uses\n")
            f.write("\n".join(list(map(lambda x: str(x[1]) + "\t" + str(x[0]), list_of_versions_since_current))))
            #print("   - a level "+ str(leastTransitiveDep) + " dependencies among "+str(len(matches))+" (possibly transitive) uses\n")
            #print("\n".join(list(map(lambda x: str(x[1]) + "\t" + str(x[0]), list_of_versions_since_current))))
        if len(list_of_versions_since_current) > 0:
            prospectiveVersion=list_of_versions_since_current[0][0]
            if prospectiveVersion != version:
                print("Analyzing ", group, ":", artifact)

                regex = "(.* "+group+":"+artifact+":[^ ]*)$"
                with open(".deps/dependencies-tree.txt", "w") as f:
                    for i in range(len(dependency_tree)):
                        if re.search(regex, dependency_tree[i]) is not None:
                            dependency_tree[i] = dependency_tree[i] + "  > " +str(prospectiveVersion)
                            #print(dependency_tree[i])
                        f.write(dependency_tree[i])
                        f.write("\n")
        #if do_input:
            #input("Press ENter")

    with open(".deps/immediate-upgrade-opportunities.txt", "w") as f:
        f.write("\n".join(list(sorted(set([d for d in dependency_tree if re.search("^  ", d) is None and re.search(">", d) is not None])))))


    print("Check the .deps/ directory")
