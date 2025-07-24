#!/bin/bash
if [ "$1" = "get-latest-putusan" ]; then
    python -m demo.api.get-latest-putusan
elif [ "$1" = "generate-tree" ]; then
    python -m demo.api.generate-tree
elif [ "$1" = "crawl-scrape-all" ]; then
    python -m demo.api.crawl-scrape-all
else
    echo "Unknown command: $1"
    exit 1
fi
