`index.html` - main file to modify page content
`templates` - folder containing various dummy html files.
`legal` - folder containing T&C and COC.
`assets` - folder containing images, css, and js


## Image optimization
```bash
# Install on your local
sudo apt install graphicsmagick-imagemagick-compat

# Convert all team photos
for file in assets/img/team/*.png; do
    convert "$file" -resize 300x300^ -gravity center -extent 300x300 -quality 80 "${file%.*}.jpg" && rm "$file"
done

# Convert all activity images
for file in assets/img/activities/*.png; do
    convert "$file" -quality 80 -resize 800x600 "${file%.*}.jpg" && rm "$file"
done

# convert a specific photo
img=assets/img/activities/3rd_mlsat.jpg
convert "$img" -quality 80 -resize 800x600 "$img"

convert "$img" -quality 80 -resize 800x600 "${img%.*}.jpg" && rm "$img"
```

### resource
we can this doc for GitHub Page DNS management: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site?platform=linux