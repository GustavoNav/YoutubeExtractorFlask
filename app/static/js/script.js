// MENU

document.addEventListener('DOMContentLoaded', () => {

const extractButton = document.getElementById('extractButton');
const dataButton = document.getElementById('dataButton');
const measurementsButton = document.getElementById('measurementsButton');

const selectedButton = localStorage.getItem('selectedButton');
if (selectedButton) {
    const button = document.getElementById(selectedButton);
    if (button) {
    button.classList.remove('inactive');
    button.classList.add('active');
    }
}

[extractButton, dataButton, measurementsButton].forEach((button) => {
    button.addEventListener('click', (event) => {
    [extractButton, dataButton, measurementsButton].forEach((b) => {
        b.classList.remove('active');
        b.classList.add('inactive');
    });

    button.classList.remove('inactive');
    button.classList.add('active');

    localStorage.setItem('selectedButton', button.id);

    setTimeout(() => {
        if (button.id === 'extractButton') {
        window.location.href = '/extract';
        } else if (button.id === 'dataButton') {
        window.location.href = '/data';
        } else if (button.id === 'measurementsButton') {
        window.location.href = '/measurements';
        }
    }, 100);
    });
});
});



// EXTRACT

function openTrendingConfirmation() {
    var modal = document.getElementById('custom_confirmation_modal');
    modal.style.display = 'block';
}

function closeTrendingConfirmation() {
    var modal = document.getElementById('custom_confirmation_modal');
    modal.style.display = 'none';
}

function submitExtractTrending() {
    var form = document.getElementById('form_extract_trending');
    showLoadingModal();
    fetch(form.action, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        var timeTaken = data.time_taken;
        hideLoadingModal();
        alert(`Tempo levado: ${timeTaken} segundos`);
    })
    .catch((error) => {
        console.error('Error:', error);
        hideLoadingModal();
    });
    closeTrendingConfirmation();
}

function openChannelsConfirmation() {
    var modal = document.getElementById('channels_confirmation_modal');
    modal.style.display = 'block';
}

function closeChannelsConfirmation() {
    var modal = document.getElementById('channels_confirmation_modal');
    modal.style.display = 'none';
    document.getElementById('channels_links').value = '';
}

function submitExtractChannels() {
    var form = document.getElementById('form_extract_channels');
    var links = document.getElementById('channels_links').value.split('\n');
    showLoadingModal();
    fetch(form.action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ links: links })
    })
    .then(response => response.json())
    .then(data => {
        var timeTaken = data.time_taken;
        hideLoadingModal();
        alert(`Tempo levado: ${timeTaken} segundos`);
    })
    .catch((error) => {
        console.error('Error:', error);
        hideLoadingModal();
    });
    closeChannelsConfirmation();
}

let secondsElapsed = 0;
let intervalTimer;

function getQueryParam(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

function startTimer() {
    intervalTimer = setInterval(() => {
        secondsElapsed++;
        document.getElementById('loading_counter').textContent = `Seconds: ${secondsElapsed}`;
    }, 1000);
}

function stopTimer() {
    clearInterval(intervalTimer);
    secondsElapsed = 0;
    document.getElementById('loading_counter').textContent = `Seconds: ${secondsElapsed}`;
}

function showLoadingModal() {
    var modal = document.getElementById('modal_loading');
    modal.style.display = 'block';
    startTimer();
}

function hideLoadingModal() {
    var modal = document.getElementById('modal_loading');
    modal.style.display = 'none';
    stopTimer();
}

window.onclick = function(event) {
    var trendingModal = document.getElementById('custom_confirmation_modal');
    var channelsModal = document.getElementById('channels_confirmation_modal');
    if (event.target == trendingModal) {
        trendingModal.style.display = "none";
        stopTimer();
    } else if (event.target == channelsModal) {
        channelsModal.style.display = "none";
        stopTimer();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const timeTaken = getQueryParam('time_taken');
    if (timeTaken) {
        alert(`Tempo levado: ${timeTaken} segundos`);
    }
});




// DATA

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('button_channels').onclick = function () {
        window.location.href = '/data';
    };
    
    document.getElementById('button_videos').onclick = function () {
        window.location.href = '/data_videos';
    };

    document.getElementById('sort_az').addEventListener('click', function() {
        sortChannels(true);
    });
    
    document.getElementById('sort_za').addEventListener('click', function() {
        sortChannels(false);
    });
    
    document.getElementById('search_input').addEventListener('input', function() {
        searchChannels();
    });

});


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('sort_videos_az').addEventListener('click', function() {
        sortVideos(true)
    });

    document.getElementById('sort_videos_za').addEventListener('click', function() {
        sortVideos(false)
    });

    document.getElementById('search_videos_input').addEventListener('input', function() {
        searchVideos()
    });
});

function sortChannels(ascending) {
    let list = document.getElementById('channel_list');
    let items = list.getElementsByClassName('channel-item');
    let itemsArray = Array.prototype.slice.call(items);

    itemsArray.sort(function(a, b) {
        let nameA = a.querySelector('.channel_name').textContent.toUpperCase();
        let nameB = b.querySelector('.channel_name').textContent.toUpperCase();
        if (nameA < nameB) {
            return ascending ? -1 : 1;
        }
        if (nameA > nameB) {
            return ascending ? 1 : -1;
        }
        return 0;
    });

    for (let i = 0; i < itemsArray.length; i++) {
        list.appendChild(itemsArray[i]);
    }
}

function searchChannels() {
    let input = document.getElementById('search_input').value.toUpperCase();
    let list = document.getElementById('channel_list');
    let items = list.getElementsByClassName('channel-item');

    for (let i = 0; i < items.length; i++) {
        let name = items[i].querySelector('.channel_name').textContent.toUpperCase();
        if (name.indexOf(input) > -1) {
            items[i].style.display = "";
        } else {
            items[i].style.display = "none";
        }
    }
}

function sortVideos(ascending) {
    let list = document.getElementById('video_list');
    let items = list.getElementsByClassName('video-item');
    let itemsArray = Array.prototype.slice.call(items);

    itemsArray.sort(function(a, b) {
        let titleA = a.querySelector('.video_title').textContent.toUpperCase();
        let titleB = b.querySelector('.video_title').textContent.toUpperCase();
        if (titleA < titleB) {
            return ascending ? -1 : 1;
        }
        if (titleA > titleB) {
            return ascending ? 1 : -1;
        }
        return 0;
    });

    for (let i = 0; i < itemsArray.length; i++) {
        list.appendChild(itemsArray[i]);
    }
}

function searchVideos() {
    let input = document.getElementById('search_videos_input').value.toUpperCase();
    let list = document.getElementById('video_list');
    let items = list.getElementsByClassName('video-item');

    for (let i = 0; i < items.length; i++) {
        let title = items[i].querySelector('.video_title').textContent.toUpperCase();
        if (title.indexOf(input) > -1) {
            items[i].style.display = "";
        } else {
            items[i].style.display = "none";
        }
    }
}



// MEANSUREMENTS

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('meansurements_channels_button').addEventListener('click', function() {
        var iframe = document.getElementById('dash_iframe');
        iframe.src = '/channels/';
    });

    document.getElementById('meansurements_videos_button').addEventListener('click', function() {
        var iframe = document.getElementById('dash_iframe');
        iframe.src = '/videos/';
    });
});
