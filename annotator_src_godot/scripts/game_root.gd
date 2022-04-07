extends Node


# Declare member variables here. Examples:
# var a = 2
# var b = "text"

var data = []

# Called when the node enters the scene tree for the first time.
func _ready():
	# load data
	
	var file = File.new()
	# selects the first probe
	file.open('res://data/source_1.tsv', File.READ)
	var lines = file.get_as_text().split("\n")
	
	file.close()
	for line in lines:
		line = line.split("\t")
		if len(line) <= 1:
			# empty line
			continue
		data.append([line[0], line[1]])
	
	next_sentence()

var word_i
var sent_i = -1
var cur_sent_words
var cur_sent_img
var cur_sent_text = ""

func next_sentence():
	sent_i += 1
	word_i = -1
	cur_sent_text = ""
	$Sentence.text = ""
	
	if sent_i >= len(data):
		game_over()
		return
		
	$Progress.text = "%d/%d" % [sent_i+1, len(data)]
	
	cur_sent_words = data[sent_i][0].split(" ")
	cur_sent_img = data[sent_i][1]
	
	if len(cur_sent_img) == 0:
		no_image()
	else:
		download_img(cur_sent_img)
	
func game_over():
	$GameOver.visible = true

func next_word():
	word_i += 1
	
	if word_i >= len(cur_sent_words):
		next_sentence()
		return
	
	cur_sent_text += " " + cur_sent_words[word_i]
	$Sentence.text = cur_sent_text

func no_image():
	$Image.texture = load("res://images/no_image.png")
	$Image.scale = Vector2.ONE
	
func download_img(filename):
	$Image.texture = load("res://images/load_image.png")
	$Image.scale = Vector2.ONE
	
	var http = HTTPRequest.new()
	add_child(http)
	var http_error = http.request("https://vilda.net/s/mmsg/img_data/%s" % filename)
	
	if http_error != OK:
		print("An error occurred in the HTTP request.")
		print(http_error)
	
	http.connect("request_completed", self, "download_img_done")
	
func download_img_done(result: int, response_code: int, headers, body):
	var img := Image.new()
	var error = img.load_jpg_from_buffer(body)
	if error != OK:
		print("Could not load the image.", error)
	var tex = ImageTexture.new()
	tex.create_from_image(img)
	
	$Image.texture = tex
	
	var scale = 300.0/$Image.texture.get_height()
	$Image.scale = Vector2(scale, scale)
