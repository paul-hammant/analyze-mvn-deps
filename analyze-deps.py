#!/usr/bin/env python

import os
import sys
import subprocess
import re
import requests
#import pysed


if not os.path.isfile(".deps") and not os.path.isdir(".deps"):
    os.mkdir(".deps")
else:
    exit()

print("Getting dependency tree for current directory")

rawoutput = subprocess.check_output(["mvn", "dependency:tree"]).decode('utf-8').split('\n')
output = []

with open(".deps/mvn-dep-tree-output.txt", "w") as mvn_dep_tree_output:
    for l in rawoutput:
        if "[INFO]" in l or "[WARNING]" in l: #if not ("Downloading" in l or "Downloaded" in l or "Progress" in l):
            mvn_dep_tree_output.write(l)
            mvn_dep_tree_output.write('\n')
            output.append(l)
        if "Total time" in l:
            break

print("Dependency tree for current directory acquired")

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

flattened_unique_gavs = [":".join(s.replace(" ", "").split(":")[:4]) for s in dependency_tree if ":" in s]
flattened_unique_gavs = sorted(list(set(flattened_unique_gavs)))
with open(".deps/flattened-unique-gavs.txt", "w") as f:
    f.write("\n".join(flattened_unique_gavs))

for l in flattened_unique_gavs:
    group, artifact, type, version = l.split(":")
    groupDir = group.replace(".", "/")
    r = requests.get("http://central.maven.org/maven2/"+ groupDir + "/" + artifact)
    try:
        list_of_versions = [re.findall(".*>(.*)/</a.*", x)[0] for x in r.text.split('\n') if "href" in x and not "maven-metadata" in x and re.search("[bB]eta", x) is None and re.search("[aA]lpha", x) is None and not ".." in x and re.search("[Rr][Cc][\.]*[0-9]* ", s) is None]
    except IndexError:
        continue
    list_of_versions = list(set(list_of_versions))
    list_of_versions.sort(reverse=True, key=lambda s: list(map(int, s.split('.'))))
    list_of_versions_with_current = list_of_versions
    current_index = 0
    for i in range(len(list_of_versions_with_current)):
        if list_of_versions_with_current[i] == version:
            list_of_versions_with_current[i] = version + " ***"
            current_index = i
    list_of_versions_since_current = list_of_versions_with_current[:current_index+1]
    with open(".deps/big-dependency-report.txt", "a") as f:
        f.write("\n========================================================================\nPresently in use: "+group+":"+artifact+"  "+ version+ "\n")
        matches=[s for s in dependency_tree if re.search(group+":"+artifact, s)]
        if len(matches) == 0:
            continue
        leastTransitiveDep = sorted(matches)[-1] 
        leastTransitiveDep = len(leastTransitiveDep) - len(leastTransitiveDep.strip())
        f.write("   - a level "+ str(leastTransitiveDep) + " dependencies among "+str(len(matches))+" (possibly transitive) uses\n")
        f.write("\n".join(list_of_versions_since_current))
    if len(list_of_versions_since_current) > 0:
        #print(list_of_versions_since_current[0])
        prospectiveVersion=list_of_versions_since_current[0]
        #print("Prospective Version: ", prospectiveVersion)
        #print("version: ", version)
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

with open(".deps/immediate-upgrade-opportunities.txt", "w") as f:
    f.write("\n".join(list(sorted(set([d for d in dependency_tree if re.search("^  ", d) is None and re.search(">", d) is not None])))))


print("Check the .deps/ directory")
