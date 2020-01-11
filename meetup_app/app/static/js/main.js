$(function() {
    let body = $('.body');
    $('.mdp.active').multiDatesPicker();
    $('.mdp.inactive').multiDatesPicker({
        addDates: parseDates($('#eventDates').val())
    });
    $('#'+$('.body').data('currentpage')).removeClass('hidden');
    let startTime = $('#startTime');
    let endTime = $('#endTime');
    let accountButton = $('#accountButton');
    let pwReset = $('#pwReset');
    let sidebar = $('.sidebar');
    let sidebarClose = $('.close');
    let sidebarError = $('.sidebarError');
    let sidebarFlash = $('.sidebarFlash');
    let pageTurn = $('.pageTurn');
    let timepickerConfig = {
        timeFormat:'h:mm p',
        interval:15,
        minTime:'0',
        maxTime:'11:59pm',
        defaultTime: '12',
        dynamic:false,
        dropdown:true,
        scrollbar:false,
        change:function() {
            let sTime = startTime.val(), eTime = endTime.val();
            if (stdToMil(sTime) > stdToMil(eTime))
                if (endTime.val() != sTime)
                    endTime.val(sTime);
            if (endTime.attr('minTime') != sTime) {
                endTime.attr('minTime', sTime);
                endTime.timepicker('option', 'minTime', sTime);
            }
        }
    }
    startTime.timepicker(timepickerConfig);
    endTime.timepicker(timepickerConfig);
    accountButton.click(function() {toggleSidebar(sidebar)});
    pwReset.click(function() {togglePwr($('#pwrDiv'))});
    sidebarClose.click(function() {toggleSidebar(sidebar)});
    if(sidebarError.children().length > 0 || sidebarFlash.children().length > 0)
        sidebar.addClass('open');
    pageTurn.prop('href', 'javascript:void(0)');
    pageTurn.click(function() {
        let tgtId = $(this).data('target'), tgt = $('#'+tgtId);
        let curId = body.data('currentpage'), cur = $('#'+curId);
        if (tgtId == curId)
            return;
        cur.addClass('hidden');
        tgt.removeClass('hidden');
        body.data('currentpage', tgtId);
    });
});

function stdToMil(time) {
    let spl = time.split(' ');
    let spl2 = spl[0].split(':');
    let h = spl2[0], m = spl2[1], s = '00';
    if (spl[1] == 'AM') {
        if (h == '12') h = '0'
    } else {
        if (h != '12') h = String(parseInt(h) + 12)
    }
    if (parseInt(h) < 10) h = '0'+h;
    return h+':'+m+':'+s;
}
function milToStd(time) {
    let spl = time.split(':');
    let h = parseInt(spl[0]), m = spl[1], s = spl[2], half = 'AM';
    if (h > 12) {
        h -= 12;
        half = 'PM';
    } else if (h == 0) h = 12;
    return String(h)+':'+m+':'+s+' '+half;
}

function togglePwr(pwrDiv) {
    if (pwrDiv.hasClass('open')) {
        pwrDiv.slideUp(500);
        pwrDiv.removeClass('open');
    } else {
        pwrDiv.slideDown(500);
        pwrDiv.addClass('open');
    }
}

function toggleSidebar(sidebar) {
    sidebar.animate({width:'toggle'},500);
    if (sidebar.hasClass('open'))
        sidebar.removeClass('open');
    else
        sidebar.addClass('open');
}

function parseDates(str) {
    let arr = str.split(',');
    arr.forEach(function(e, i) {arr[i] = new Date(e)});
    console.log(arr);
    return arr;
}

function setCookie(name,val,exp) {
    let expires = '';
    if (exp) {
        let date = new Date();
        date.setTime(date.getTime() + (exp*24*60*60*1000));
        expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + (val || '')  + expires + '; path=/';
}
function getCookie(name) {
    let nameEQ = name + '=';
    let ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {
    document.cookie = name+'=; Max-Age=-99999999;';
}
function onMdpChange() {
    $('#dates').val($('#mdp').multiDatesPicker('getDates', 'string').toString());
}