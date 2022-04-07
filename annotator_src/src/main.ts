$("#button_0").on("click", () => rate(0));
$("#button_1").on("click", () => rate(1));
$("#button_2").on("click", () => rate(2));
$("#button_3").on("click", () => rate(3));
$("#button_4").on("click", () => rate(4));

var data: any[] = []
let sent_i = -1
let word_i = -1
let cur_sent_words: string[] = []
let cur_sent_text = ""

function rate(value: number) {
    next_word()
}

function load_data() {
    $.getJSON(
        "data/queue_01.json",
        (new_data) => {
            data = new_data
            console.log(data)
            update_progress()
            next_sentence()
        }
    )
}

function update_progress() {
    $("#progress").text((sent_i + 1).toString() + "/" + (data.length).toString())
}

function next_sentence() {
    sent_i += 1
    if (sent_i >= data.length) {
        alert("Annotations done.")
        return
    }

    cur_sent_text = ""
    word_i = -1

    $.getJSON(
        "https://vilda.net/s/mmsg/img_data/" + data[sent_i]["id"] + "/meta.json"
    ).done((metadata) => {
        cur_sent_words = metadata["caption"][0].split(" ")

        $("#multimodality").html("")
        $("#config_info").html("Mode: " + data[sent_i]["config"])

        if (data[sent_i]["config"] == "original") {
            $("#multimodality").append("<img src='https://vilda.net/s/mmsg/img_data/" + data[sent_i]["id"].toString() + "/original.jpg'>")
        } else if (data[sent_i]["config"] == "labels_all") {
            console.log("<img src='https://vilda.net/s/mmsg/img_data/" + data[sent_i]["id"].toString() + "/labels_all.jpg'>")
            $("#multimodality").append("<img src='https://vilda.net/s/mmsg/img_data/" + data[sent_i]["id"].toString() + "/labels_all.jpg'>")
        } else if (data[sent_i]["config"] == "clear_all") {
            $("#multimodality").append("<img src='https://vilda.net/s/mmsg/img_data/" + data[sent_i]["id"].toString() + "/clear_all.jpg'>")
        } else if (data[sent_i]["config"] == "clear_crop") {
            for (let i = metadata["labels"].length - 1; i >= 0; i--) {
                $("#multimodality").append("<img src='https://vilda.net/s/mmsg/img_data/" + data[sent_i]["id"].toString() + "/clear_crop_" + i.toString() + ".jpg'>")
            }
        } else if (data[sent_i]["config"] == "labels_crop") {
            for (let i = metadata["labels"].length - 1; i >= 0; i--) {
                console.log(metadata["labels"][i])
                $("#multimodality").append("<img src='https://vilda.net/s/mmsg/img_data/" + data[sent_i]["id"].toString() + "/labels_crop_" + i.toString() + ".jpg'>")
            }
        } else if (data[sent_i]["config"] == "labels_text") {
            $("#multimodality").html(metadata["labels"].map((label: string) => label.split(" ")[0]).join(", "))
        } else if (data[sent_i]["config"] == "no_image") {
            $("#multimodality").append("<img src='img/no_image.png'>")
        }
        update_sentence_display()
    })
    update_progress()
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