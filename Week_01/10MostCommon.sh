cat SomeText.rtf | tr ' '  '\012' | tr '[:upper:]' '[:lower:]' | tr -d '[:punct:]' | grep -v '[^a-z]' | sort | uniq -c | sort -rn | head > 10MostCommon.txt
