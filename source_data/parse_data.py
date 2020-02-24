import parser

data = parser.parse("./nustem.WordPress.2020-02-24.xml")

# print(data['posts'])

posts = data['posts']

# Output to local directory for testing
output_path = 'content/'

# DANGER DANGER DANGER
# Output directly to the Hugo content directory. Will silently overwrite world!
# output_path = '../careers/content/posts/'

for t in data['posts']:
    this_file = output_path + t['post_name'] + '.md'
    myfile = open(this_file, 'w')
    print("+++", file=myfile)
    print("title = '" + t['title'] + "'", file=myfile)
    # print("date = '" + t['pub_date'] + "'", file=myfile)
    print("tags =", t['tags'], file=myfile)
    print("categories =", t['categories'], file=myfile)
    print("menu = \"main\"", file=myfile)
    print("+++", file=myfile)
    print("", file=myfile)
    print(t['content'], file=myfile)
    myfile.close()
    # print("TITLE: ", t['title'])
    # print(t['content']) # Main description copy (includes attributes line as last line)
    # print(t['post-date'])
    # print("TAGS: ", t['tags'])
    # print("CATEGORIES: ", t['categories'])

# 'title'
# 'link'
# 'pub_date'
# 'creator'
# 'guid'
# 'description'
# 'content'
# 'excerpt'
# 'post_id'
# 'post_date'
# 'post_date_gmt'
# 'status'
# 'post_parent'
# 'menu_order'
# 'post_type'
# 'post_name' # slug
# 'categories': []
# 'is_sticky'
# 'ping_status'
# 'post_password'
# 'tags': []
# 'postmeta'
# 'comments'
