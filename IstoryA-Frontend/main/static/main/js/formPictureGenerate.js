$(document).ready(function() {
    $("#submitGeneratePicture1").click(function () {
        var x = $("#generatePicture1").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture2").click(function () {
        var x = $("#generatePicture2").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
   $("#submitGeneratePicture3").click(function () {
        var x = $("#generatePicture3").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture4").click(function () {
        var x = $("#generatePicture4").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
   $("#submitGeneratePicture5").click(function () {
        var x = $("#generatePicture5").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture6").click(function () {
        var x = $("#generatePicture6").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture7").click(function () {
        var x = $("#generatePicture7").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture8").click(function () {
        var x = $("#generatePicture8").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture9").click(function () {
        var x = $("#generatePicture9").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture10").click(function () {
        var x = $("#generatePicture10").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture11").click(function () {
        var x = $("#generatePicture11").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
    $("#submitGeneratePicture12").click(function () {
        var x = $("#generatePicture12").serializeArray();
        let formData = new FormData();
        formData.append('text_id', x[0].value);
        formData.append('case_id', x[1].value);
        formData.append('storyboard_id', x[2].value);
        const request = new Request('/get_text_by_id/', {method: 'POST', body: formData, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
        fetch(request)
            .then(response => response.json())
            .then(result => {
                result = JSON.stringify(result)
                result = result.substring(11)
                resultLength = result.length -2
                result = result.substring(0,resultLength)
                $.ajax({
                    type: 'POST',
                    url: 'http://192.168.1.55:5000/picture_generation',
                    data: {"text" : result},
                    dataType: 'jsonp',
                    success: myCallback
                });
                function myCallback(result) {
                    alert(result)
                }
            })
    });
});



