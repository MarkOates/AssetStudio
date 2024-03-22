# General technique take from: https://www.zenrows.com/blog/web-scraping-ruby#parse-html

# Prerequisites (may require sudo):
# ruby -v
# gem install httparty
# gem install nokogiri
# gem install pry #(? - didn't actually install at the time of this writing, was already installed)

require "httparty"
require "nokogiri"
require "pry"


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

def print_element_tree(element, level = 0)
  class_names = element.attribute('class')&.value || ""
  puts "  " * level + "#{element.name} - #{class_names}"
  element.children.each do |child|
    print_element_tree(child, level + 1)
  end
end

document = Nokogiri::HTML(file_contents)
num_elements = document.css('*').size
puts "File contents parsed successfully."
puts "   - Number of elements: #{num_elements}"
# To view the document structure:
#print_element_tree(document)


# Parse the document

# TODO: continue parsing individual elements
html_products = document.css("div.game_cell")
# To view the structure of elements in "game_cell":
#print_element_tree(document)


# Load the document contents into a meaningful object

AssetProduct = Struct.new(:name, :download_link, :author_name, :author_handle, :asset_pack_url_slug)
asset_products = []

html_products.each do |html_product|
  # To inspect
  #binding.pry

  # Extract the data from the document
  name = html_product.css(".game_title").children.first.children.first.to_s
  download_link = html_product.css("a").first.attribute("href").value
  author_name = html_product.css(".game_author").children.first.children.to_s

  # Parse out url data
  match_data = download_link.match(%r{https://([^\.]+)\.itch\.io/([^/]+)/?})
  author_handle = match_data[1];
  asset_pack_url_slug = match_data[2];

  # Add the asset to our final set of objects
  asset_product = AssetProduct.new(name, download_link, author_name, author_handle, asset_pack_url_slug)
  asset_products.push(asset_product)
end


# Format our scraped data for something useful

Author = Struct.new(:name, :author_handle)
authors = Set.new

# Show assets packs
puts "= Asset Packs ==========="
asset_products.each do |asset_product|
  # TODO
  puts "#{asset_product.name} • #{asset_product.author_name} (#{asset_product.author_handle}) • #{asset_product.download_link}"
  authors << Author.new(asset_product.author_name, asset_product.author_handle)
end

# Show authors
puts "= Authors ==========="
authors.each do |author|
  puts "#{author.name} • #{author.author_handle}"
end

# Show report
puts "= Result ==========="
puts "   - Number of asset packs: #{asset_products.size}"
puts "   - Number of authors: #{authors.size}"



