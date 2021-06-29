$(document).ready(function() {
    var ip = 'http://10.0.2.97:5000/picture_generation'
    $("#submit-generate-picture-1").click(function () {
        var x = $("#generate-picture-1").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {});
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-2").click(function () {
        var x = $("#generate-picture-2").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
   $("#submit-generate-picture-3").click(function () {
        var x = $("#generate-picture-3").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-4").click(function () {
        var x = $("#generate-picture-4").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
   $("#submit-generate-picture-5").click(function () {
        var x = $("#generate-picture-5").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-6").click(function () {
        var x = $("#generate-picture-6").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-7").click(function () {
        var x = $("#generate-picture-7").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-8").click(function () {
        var x = $("#generate-picture-8").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-9").click(function () {
        var x = $("#generate-picture-9").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-10").click(function () {
        var x = $("#generate-picture-10").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-11").click(function () {
        var x = $("#generate-picture-11").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
    $("#submit-generate-picture-12").click(function () {
        var x = $("#generate-picture-12").serializeArray();
        if(x[0].value == "choose"){
            $('#error-choose').modal('show')
        }else{
            let formData = new FormData();
            formData.append('text_id', x[0].value);
            formData.append('case_id', x[1].value);
            formData.append('storyboard_id', x[2].value);
            const request = new Request('/get_text_by_id/', {
                method: 'POST',
                body: formData,
                headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
            });
            fetch(request)
                .then(response => response.json())
                .then(result => {
                    result = JSON.stringify(result)
                    result = result.substring(11)
                    resultLength = result.length - 2
                    result = result.substring(0, resultLength)
                    let formDataCreatePicture = new FormData();
                    formDataCreatePicture.append('text', result);
                    formDataCreatePicture.append('case_id', x[1].value);
                    formDataCreatePicture.append('storyboard_id', x[2].value);
                    const request2 = new Request('/create_picture/', {
                        method: 'POST',
                        body: formDataCreatePicture,
                        headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                    });
                    fetch(request2)
                        .then(response => response.json())
                        .then(result => {
                        });
                    $.ajax({
                        type: 'POST',
                        url: ip,
                        data: {
                            "text": result,
                            "storyboard_id": x[2].value,
                            "case_id": x[1].value,
                            "owner_id": x[3].value
                        },
                        dataType: 'jsonp'
                    });
                });
        }
    });
});



