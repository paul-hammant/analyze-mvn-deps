#!/bin/bash

#
# Copyright Paul Hammant, 2018
# MIT license
#

set -e

if ! [ -d ".deps" ]; then
  mkdir .deps
fi

echo "Getting dependency tree for current directory"
# do downloads first...
mvn dependency:tree > .deps/mvn-dep-tree-output.txt
mvn dependency:tree | sed '/Total time/q' > .deps/mvn-dep-tree-output.txt # before generating smallest report
echo "Dependency tree for current directory acquired"

cat .deps/mvn-dep-tree-output.txt | sed 's/|/ /g' | sed 's/+-/  /' | sed 's/\\-/  /' | sed 's/\[INFO\]//' | sed /^---/d \
    | sed /:/!d | sed /:$/d | sed '/Total time/d' | sed /\[WARNING[]]/d \
    | sed 's/   / /g' | sed 's/^ //' | sed /::/d \
    | sed 's/maven-dependency-plugin:[0-9\.]*:tree (default-cli) @ //' > .deps/dependencies-tree.txt

cat .deps/dependencies-tree.txt | sed 's/ //g' | grep ":" | cut -d':' -f 1,2,3,4 | sort | uniq > .deps/flattened-unique-gavs.txt

echo "" > .deps/big-dependency-report.txt

while IFS=: read -r group artifact type version
do
    groupDir="$(sed 's/\./\//g' <<<$group)"

    curl -s -o .deps/curl-output.txt -L "http://central.maven.org/maven2/$groupDir/$artifact"

    cat .deps/curl-output.txt | pr -t -e=2 | sed 's/\-         \-/unknown-date unknown:time/g' | sed 's/ \- //g' \
      | sed -E -e 's/[[:blank:]]+/ /g' | sed 's/\<//g' | sed 's/\"/ /g' | sed 's/^a //' | sed 's/\>//g' \
      | grep href | sed '/maven-metadata/d' | sed 's/.*title= //' | sed '/\.\./d' | grep ':' \
      | sed -E 's/(.*) (.*) (.*) (.*) (.*) (.*) (.*)/\5 \6 \1/' \
      | sed 's/href //g' | sed 's/\///' | sed '/-[aA]lpha[\.]*[0-9]* /d' | sed '/-[bB]eta[\.]*[0-9]* /d' \
      | sed '/-[Rr][Cc][\.]*[0-9]* /d' | sed '/-SNAPSHOT /d' \
      | sed 's/  title$//' | sort -nr | uniq > .deps/tmp_list_of_versions.txt

    cat .deps/tmp_list_of_versions.txt | sed "s/ $version$/ $version \*\*\*/" > .deps/tmp_list_of_versions_with_current_indicated.txt

    cat .deps/tmp_list_of_versions_with_current_indicated.txt | sed "/ $version \*\*\*$/q" > .deps/tmp_list_of_versions_since_current.txt

    printf "\n========================================================================\nPresently in use: $group:$artifact  $version\n" >> .deps/big-dependency-report.txt

    matches=$(cat .deps/dependencies-tree.txt | grep "$group:$artifact")
    matchesCount=$(echo "$matches" | wc -l | tr -d '[:space:]')
    leastTransitiveDep=$(echo "$matches" | sort | tail -1 | tr -cd ' ' | wc -m | sed 's/ *//g')
    printf "   - a level $leastTransitiveDep dependencies among $matchesCount (possibly transitive) uses\n" >> .deps/big-dependency-report.txt

    cat  .deps/tmp_list_of_versions_since_current.txt >> .deps/big-dependency-report.txt

    prospectiveVersion=$(cat .deps/tmp_list_of_versions_since_current.txt | head -n 1 | cut -d ' ' -f 4)

    if ! [ "$version" == "$prospectiveVersion" ]
    then
        echo "Analyzing ${group}:${artifact}"
        # Dammit, sed -i has no common args for Mac and Linux
        cat .deps/dependencies-tree.txt | sed -E "s/(.* ${group}:${artifact}:[^ ]*)$/\1  \> ${prospectiveVersion}/" > .deps/dependencies-tree.txtNEW
        mv .deps/dependencies-tree.txtNEW .deps/dependencies-tree.txt # could have used sponge but may not be installed.
    fi

done < .deps/flattened-unique-gavs.txt

cat .deps/dependencies-tree.txt | sed '/^  /d' | grep '>' | sort | uniq > .deps/immediate-upgrade-opportunities.txt

rm .deps/curl-output.txt
rm .deps/tmp_list_of_versions_since_current.txt
rm .deps/tmp_list_of_versions.txt
rm .deps/tmp_list_of_versions_with_current_indicated.txt

echo "Check the .deps/ directory"