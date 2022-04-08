import { DEVMODE } from "./globals"
export var UID: string
import { load_data, load_meta, log_sentence, IMGDATA_ROOT } from './connector'

$("#button_0").on("click", () => rate(0))
$("#button_1").on("click", () => rate(1))
$("#button_2").on("click", () => rate(2))
$("#button_3").on("click", () => rate(3))
$("#button_4").on("click", () => rate(4))

var data: any[] = []
let sent_i = -1
let word_i = -1
let cur_sent_words: string[] = []
let cur_sent_text = ""
let sent_data: { sent: string, time: number, config: string, id: string, ratings: [number, number][] } | null = null
let prev_time = Date.now()
let loaded = false

function rate(value: number) {
    let new_time = Date.now()
    sent_data!.ratings.push([new_time - prev_time, value])
    prev_time = new_time
    next_word()
}

function update_progress() {
    $("#progress").text((sent_i + 1).toString() + "/" + (data.length).toString())
}

function next_sentence() {
    sent_i += 1
    if (sent_i >= data.length) {
        alert("Annotations done, please wait a few seconds after closing this alert to allow for data synchronization.")
        sent_i = 0
    }


    cur_sent_text = ""
    word_i = -1

    load_meta(data[sent_i]["id"]).then((metadata) => {
        if (sent_data != null) {
            // log previous sentence if not null
            log_sentence(sent_data)
        }
        // clear local logs
        sent_data = { sent: metadata["caption"][0], time: Date.now(), config: data[sent_i]["config"], id: data[sent_i]["id"], ratings: [] }
        prev_time = Date.now()

        cur_sent_words = metadata["caption"][0].split(" ")

        $("#multimodality").html("")
        $("#config_info").html("Mode: " + data[sent_i]["config"])

        if (data[sent_i]["config"] == "original") {
            $("#multimodality").append("<img src='" + IMGDATA_ROOT + data[sent_i]["id"].toString() + "/original.jpg'>")
        } else if (data[sent_i]["config"] == "labels_all") {
            $("#multimodality").append("<img src='" + IMGDATA_ROOT + data[sent_i]["id"].toString() + "/labels_all.jpg'>")
        } else if (data[sent_i]["config"] == "clear_all") {
            $("#multimodality").append("<img src='" + IMGDATA_ROOT + data[sent_i]["id"].toString() + "/clear_all.jpg'>")
        } else if (data[sent_i]["config"] == "clear_crop") {
            for (let i = metadata["labels"].length - 1; i >= 0; i--) {
                $("#multimodality").append("<img src='" + IMGDATA_ROOT + data[sent_i]["id"].toString() + "/clear_crop_" + i.toString() + ".jpg'>")
            }
        } else if (data[sent_i]["config"] == "labels_crop") {
            for (let i = metadata["labels"].length - 1; i >= 0; i--) {
                $("#multimodality").append("<img src='" + IMGDATA_ROOT + data[sent_i]["id"].toString() + "/labels_crop_" + i.toString() + ".jpg'>")
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

    // last word
    if (word_i == cur_sent_words.length - 1) {
        $("#button_next").show();
        $("#buttons_rate").hide();
    }

    cur_sent_text += " " + cur_sent_words[word_i]
    update_sentence_display()
}

$("#button_next").on("click", () => {
    if (!loaded) {
        return
    }
    $("#button_next").hide();
    $("#buttons_rate").show();
    next_sentence()
})

load_data().then((new_data) => {
    data = new_data
    update_progress()
    loaded = true
})

if (DEVMODE) {
    UID = "vilda_devtest"
} else {
    let UID_maybe = null
    while (UID_maybe == null) {
        UID_maybe = prompt("Enter your user id:")
    }
    UID = UID_maybe!
}

console.log("Starting session with UID:", UID)