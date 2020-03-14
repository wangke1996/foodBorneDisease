import reqwest from "reqwest";

const serverURL = 'http://192.168.3.140:6006/';

function wrapUrl(url, randParam = true) {
    let trueURL = serverURL + url;
    if (randParam)
        trueURL += '?time=' + (new Date().getTime());
    return trueURL;
}

function postData(url, data, callback) {
    reqwest({
        url: wrapUrl(url),
        method: 'post',
        type: 'json',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: (d) => callback(d.response),
        error: (d) => callback(d.response),
    })
}

function getData(url, callback, data = {}) {
    reqwest({
        url: wrapUrl(url),
        type: 'json',
        method: 'get',
        data: data,
        contentType: 'application/json',
        success: callback,
    });
}

export function getAnswer(messageList, callback) {
    // getData('getAnswer', callback, JSON.stringify(messageList));
    postData('getAnswer', messageList, callback);
}

export function getBugs(callback) {
    getData('getBugs', d => callback([d]));
}

export function getBugDetail(bugKey, callback) {
    getData('getBugDetail', callback, {bugKey});
}