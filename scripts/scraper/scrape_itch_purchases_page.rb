# General technique take from: https://www.zenrows.com/blog/web-scraping-ruby#parse-html

# Prerequisites (may require sudo):
# ruby -v
# gem install httparty
# sudo gem install nokogiri

require "httparty"
require "nokogiri"


# Obtain the file contents

file_path = "/Users/markoates/Assets/purchases_list-Mar_22_2024-01.txt"
File.exist?(file_path) || abort("File \"#{file_path}\" not found!")

file_contents = File.read(file_path)

# Count the number of lines in the file
num_lines = file_contents.lines.count

# Count the number of characters in the file
num_characters = file_contents.length

puts "\"#{file_path}\" found successfully."
puts "   - Number of lines: #{num_lines}"
puts "   - Number of characters: #{num_characters}"


# Load the document

document = Nokogiri::HTML(file_contents)
num_elements = document.css('*').size
puts "File contents parsed successfully."
puts "   - Number of elements: #{num_elements}"

# Parse the document

# TODO: continue parsing individual elements
html_products = document.css("div.purchase_game_widget")

