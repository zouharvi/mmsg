$("#button_0").on("click", () => rate(0));
$("#button_1").on("click", () => rate(1));
$("#button_2").on("click", () => rate(2));
$("#button_3").on("click", () => rate(3));
$("#button_4").on("click", () => rate(4));

var data : any[] = []
let sent_i = -1
let word_i = -1
let cur_sent_words : string[] = []
let cur_sent_text = ""

function rate(value: number) {
    next_word()
}


function load_data() {
    $.getJSON(
        "data/queue_01.json",
        (new_data) => {
            data = new_data
            update_progress()
            next_sentence()
        }
        )
    }
    
function update_progress() {
    $("#progress").text((sent_i+1).toString() + "/" + (data.length).toString())
}

function next_sentence() {
    
    sent_i += 1
    if (sent_i >= data.length) {
        alert("Annotations done.")
    }
    cur_sent_text = ""
    cur_sent_words = data[sent_i]["sent"].split(" ")
    word_i = -1
    
    $("#multimodality").html("")
    data[sent_i]["imgs"].forEach((img : string)=> {        
        console.log(img)
        $("#multimodality").append("<img src='https://vilda.net/s/mmsg/img_data/" + img + "'>")
    })
    if (data[sent_i]["imgs"].length == 0) {
        $("#multimodality").append("<img src='img/no_image.png'>")
    }
    
    update_progress()
    update_sentence_display()
}

function update_sentence_display() {
    $("#sentence").text(cur_sent_text + " ____")
}


function next_word() {
    word_i += 1
    if (word_i >= cur_sent_words.length) {
        next_sentence()
        return
    }

    cur_sent_text += " " + cur_sent_words[word_i]
    update_sentence_display()
}

load_data()


// var word_i
// var sent_i = -1
// var cur_sent_words
// var cur_sent_img
// var cur_sent_text = ""

// func next_sentence():
// 	sent_i += 1
// 	word_i = -1
// 	cur_sent_text = ""
// 	$Sentence.text = ""
	
// 	if sent_i >= len(data):
// 		game_over()
// 		return
		
// 	$Progress.text = "%d/%d" % [sent_i+1, len(data)]
	
// 	cur_sent_words = data[sent_i][0].split(" ")
// 	cur_sent_img = data[sent_i][1]
	
// 	if len(cur_sent_img) == 0:
// 		no_image()
// 	else:
// 		download_img(cur_sent_img)
	
// func game_over():
// 	$GameOver.visible = true

// func next_word():
// 	word_i += 1
	
// 	if word_i >= len(cur_sent_words):
// 		next_sentence()
// 		return
	
// 	cur_sent_text += " " + cur_sent_words[word_i]
// 	$Sentence.text = cur_sent_text

// func no_image():
// 	$Image.texture = load("res://images/no_image.png")
// 	$Image.scale = Vector2.ONE
	
// func download_img(filename):
// 	$Image.texture = load("res://images/load_image.png")
// 	$Image.scale = Vector2.ONE
	
// 	var http = HTTPRequest.new()
// 	add_child(http)
// 	var http_error = http.request("https://vilda.net/s/mmsg/img_data/%s" % filename)
	
// 	if http_error != OK:
// 		print("An error occurred in the HTTP request.")
// 		print(http_error)
	
// 	http.connect("request_completed", self, "download_img_done")
	
// func download_img_done(result: int, response_code: int, headers, body):
// 	var img := Image.new()
// 	var error = img.load_jpg_from_buffer(body)
// 	if error != OK:
// 		print("Could not load the image.", error)
// 	var tex = ImageTexture.new()
// 	tex.create_from_image(img)
	
// 	$Image.texture = tex
	
// 	var scale = 300.0/$Image.texture.get_height()
// 	$Image.scale = Vector2(scale, scale)
