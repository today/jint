// renren.com Robot
// version 0.1 BETA!
// 2009-6-24 14:37:54
// Copyright (c) 2005, Jin Tian
// Released under the GPL license
// http://www.gnu.org/copyleft/gpl.html
//
// --------------------------------------------------------------------
//
// This is a Greasemonkey user script.
//
// To install, you need Greasemonkey: http://greasemonkey.mozdev.org/
// Then restart Firefox and revisit this script.
// Under Tools, there will be a new menu item to "Install User Script".
// Accept the default configuration and install.
//
// To uninstall, go to Tools/Manage User Scripts,
// select "Hello World", and click Uninstall.
//
// --------------------------------------------------------------------
//
// ==UserScript==
// @name          renren Farmer
// @namespace     http://jint.org/gs/
// @description   example script to alert "Hello world!" on every page
// @include       http://m.renren.com/*
// @include       http://home.renren.com/*
// @include       http://mapps.renren.com/*
// @include       http://mapps.renren.com/*
// @exclude       http://diveintogreasemonkey.org/*
// @exclude       http://www.diveintogreasemonkey.org/*
// ==/UserScript==

//alert("Script Start");

var flag_SH = GM_getValue('SH', true);   // 是否自动收获
var flag_WH = GM_getValue('WH', true);   // 是否自动维护：锄草，浇水，杀虫
var flag_HF = GM_getValue('HF', true);   // 是否自动化肥
flag_str = "" + flag_SH + "," + flag_WH + "," + flag_HF
//alert( flag_str );

var allLinks, thisLink;
allLinks = document.evaluate(
    '//a[@href]',
    document,
    null,
    XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE,
    null);

var i = 0;
var flag = 0;

var thisHref = window.location.href;

// 检查是否需要登录，如果是，登之
allBtns = document.evaluate(
    '//input[@type]',
    document,
    null,
    XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE,
    null);
for (i = 0; i < allBtns.snapshotLength; i++) {
    thisBtn = allBtns.snapshotItem(i);
    valueText = thisBtn.value ;
    if( valueText == '登录'){
        // 触发click事件
        document.forms[0].submit();
        return;
    }
}
//alert('1')

// 先检查浏览器是否被导向了其他地址，如果是，跳转到农场
//alert(thisHref.indexOf("mapps.renren.com") );
if( thisHref.indexOf("mapps.renren.com") < 0 ){
    //alert("");
    window.location.href = "http://mapps.renren.com/happyfarm/";
}

for (i = 0; i < allLinks.snapshotLength && flag==0; i++) {
    thisLink = allLinks.snapshotItem(i);

    linkText = thisLink.href ;        
    var actionText = thisLink.text;
    if( actionText == '这里'){
        // 出错了，就等等再试验
        window.tempHrefString = linkText;
        window.setTimeout(
            function() { window.location.href = window.tempHrefString; }, 
            10000 + Math.floor( Math.random() * 2000 ) );
        flag=1
    }
}

for (i = 0; flag_SH && i < allLinks.snapshotLength && flag==0; i++) {
    thisLink = allLinks.snapshotItem(i);
    
    linkText = thisLink.href ;        
    var actionText = thisLink.text;
    if( actionText == '收获'){
        // 收获要尽量快
        window.tempHrefString = linkText;
        window.setTimeout(
            function() { window.location.href = window.tempHrefString; }, 
            Math.floor( Math.random() * 1000 ) );
        flag = 2;
    }
}

for (i = 0; flag_WH && i < allLinks.snapshotLength && flag==0; i++) {
    thisLink = allLinks.snapshotItem(i);
    
    linkText = thisLink.href ;        
    var actionText = thisLink.text;
    if( actionText == '除草' || actionText == '除虫' || actionText == '浇水'){
        // 除草 除虫 浇水 都不急
        window.tempHrefString = linkText;
        window.setTimeout(
            function() { window.location.href = window.tempHrefString; }, 
            1000 + Math.floor( Math.random() * 2000 ) );
        flag = 3;
        break;
        
    }
}    
for (i = 0; i < allLinks.snapshotLength && flag==0; i++) {
    thisLink = allLinks.snapshotItem(i);
    
    linkText = thisLink.href ;        
    var actionText = thisLink.text;
    if( (actionText == '播种' || actionText == '铲除' || actionText == '种植' )&& flag == 0){
        // 播种也不能延迟
        window.tempHrefString = linkText;
        window.setTimeout(
            function() { window.location.href = window.tempHrefString; }, 
            Math.floor( Math.random() * 1000 ) );
        flag=4;
        break;
    }
}

for (i = 0; flag_HF && i < allLinks.snapshotLength && flag==0; i++) {
    thisLink = allLinks.snapshotItem(i);
    
    linkText = thisLink.href ;        
    var actionText = thisLink.text;
    if( (actionText == '施肥' || actionText == '使用一袋') && flag == 0){
        // 最后再施肥
        window.tempHrefString = linkText;
        window.setTimeout(
            function() { window.location.href = window.tempHrefString; }, 
            1000 + Math.floor( Math.random() * 1000 ) );
        flag=5
        break;
    }
}  

// Auto Reload
// alert("");
if( flag==0 ){
    window.setTimeout(
        function() { window.location.href = "http://mapps.renren.com/happyfarm/"; }, 
        600000 + Math.floor( Math.random() * 100000 ));
}

var newElement = document.createElement('div');
var appendHtml = "<form name='form_gs' method='get' action='' >"
                +" <input type='text' id='t_gs' name='t_gs' value='"+flag_str+"' />"
                +" <input type='button' id='b_gs' name='b_gs' value='save' /></form>"
newElement.innerHTML = "" + new Date() + appendHtml; 
document.body.insertBefore(newElement, document.body.firstChild);

b_gs = document.getElementById("b_gs");
b_gs.addEventListener('click', function(event) {
    //alert('start config save');
    
    flag = document.getElementById("t_gs").value;
    
    fs = flag.split(",");

    if( 'true' == fs[0] ){
        GM_setValue('SH', true); 
    }else{
        GM_setValue('SH', false); 
    }
    
    if( 'true' == fs[1] ){
        GM_setValue('WH', true); 
    }else{
        GM_setValue('WH', false); 
    }
    
    if( 'true' == fs[2] ){
        GM_setValue('HF', true); 
    }else{
        GM_setValue('HF', false); 
    }
}, true);



