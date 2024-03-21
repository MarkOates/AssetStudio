#!/bin/sh

#CSV_URL="https://docs.google.com/spreadsheets/d/1vedD3jUY7_w5pRCI3hUWNhPzehzoGecKdoAmlOqbAig/edit#gid=0"
# CSV_URL="https://docs.google.com/spreadsheets/d/1vedD3jUY7_w5pRCI3hUWNhPzehzoGecKdoAmlOqbAig/export?exportFormat=csv"
CSV_URL="https://docs.google.com/spreadsheets/d/1qWKh4-TxAhIQEa7LUg-ih9xsCWANSLRtvwzVyYH0HIM/export?exportFormat=csv"
# edit#gid=646986983"
# CSV_URL="https://docs.google.com/spreadsheets/d/1qWKh4-TxAhIQEa7LUg-ih9xsCWANSLRtvwzVyYH0HIM/edit#gid=646986983"
# curl -L "https://docs.google.com/spreadsheets/d/1By-EzGexU9DHZgtKFR6XwftfL13Su9Kff4KFcpRR7dg/export?exportFormat=csv" --output /Users/markoates/Repos/SurviveTheCity/bin/data/levels/universe.csv


curl -L "$CSV_URL" --output /Users/markoates/Assets/assets_db.csv


