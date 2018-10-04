IMGUR_UPLOAD="https://api.imgur.com/3/image"
GITHUB_API="https://api.github.com"

upload_image() {
	DATA=$(cat $1 | base64)
	curl -s --request POST \
	  --url $IMGUR_UPLOAD \
	  --header "Authorization: Client-ID $IMGUR_ID" \
	  --header 'content-type: multipart/form-data' \
	  --form image=$DATA | tee /dev/fd/2 | jq -r '.["data"]["link"]'
}

post_comment() {
	BODY="{\"body\": \"$1\"}"
	curl -s --request POST \
	  --url "$GITHUB_API/repos/$TRAVIS_PULL_REQUEST_SLUG/issues/$TRAVIS_PULL_REQUEST/comments" \
	  --header "Authorization: token $GITHUB_TOKEN" \
	  --header 'content-type: application/json' \
	  --data "$BODY"
}

COMMENT=""

FAILED_IMAGES=$(find . -regex '.*assertion-failures.*\.png')
if [ -n "$FAILED_IMAGES" ]; then
	COMMENT+="Some assertions failed!\n"
fi

for filename in $FAILED_IMAGES; do
	COMMENT+=$filename
	COMMENT+="![]($(upload_image $filename))\n"
done

PASS_IMAGES=$(find . -regex '.*assertion-passes.*\.png')
PASS_COMMENT=""
for filename in $PASS_IMAGES; do
	PASS_COMMENT+=$filename
	PASS_COMMENT+="![]($(upload_image $filename))\n"
done

COMMENT+="<details><summary>Passed assertions</summary>\n<p>\n\n$PASS_COMMENT\n</p></details>"
echo "Commenting"
post_comment "$COMMENT"