import { DEVMODE } from './globals'
import { UID } from './main'

let SERVER_LOG_ROOT = DEVMODE ? "http://127.0.0.1/" : "https://quest.ms.mff.cuni.cz/mmsg/"
export let IMGDATA_ROOT = "https://vilda.net/s/mmsg/img_data/"

export async function load_data(): Promise<any> {
    console.log(UID)
    let result = await $.getJSON(
        "baked_queues/" + UID + ".json",
    )
    return result
}

export async function load_meta(id: string): Promise<any> {
    let result = await $.getJSON(
        IMGDATA_ROOT + id + "/meta.json"
    )
    return result
}

export async function log_sentence(data: any): Promise<any> {
    let result = await $.ajax(
        SERVER_LOG_ROOT + "log",
        {
            data: JSON.stringify({...data, uid: UID}),
            type: 'POST',
            contentType: 'application/json',
        }
    )
    return result
}