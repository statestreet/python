/**
 * check value is null or not
 * return true: value is not null
 * return false:  value is null
 */
var nullCheck = function(value)
{
    var patrn = /^\s*$/
    if(value == null || patrn.exec(value)) {
        return false
    }

    return true;
}

/**
 * to request url with ajax
 * callback: function to process the request result
 * url： the url to requst 
 */
function request(url, callback) 
{
    var xmlhttp;
    var txt, x, i;
    if(window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {// code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
        if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            xmlDoc = xmlhttp.responseText;
            result = xmlDoc
            callback(result)
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

/**
 * check value is number or not
 * return true value is number
 * return false value is not number
 */
var numCheck = function(value) 
{
    var regExp = /^[1-9]\d*$/
    if(value == null || !regExp.exec(value)) {
        return false;
    }

    return true;
}

/**
 * get comment in the div block with id
 * id: the id of the div block
 */
var getComment = function(id) 
{
    comment = document.getElementById(id)
    childs = comment.childNodes
    for(var i = 0; i < childs.length; i++) {
        child = childs[i]
        if(child.nodeType == 8) {
            return child.nodeValue
            break
        }
    }
}

