var fs = require('fs');

var filename = 'data/links.json';
var url_toplevel = 'http://eresources.nlb.gov.sg/webarchives/wayback/20070223201456/http://app.sgdi.gov.sg/'

var obj = JSON.parse(fs.readFileSync(filename));
var outputobj = {};

var min = 'ministries';
var oos = 'oos';
var sb = 'sb';
var oth = 'others';

var result = {};
result = parse(min);
outputobj[min] = result;
result = parse(oos);
outputobj[oos] = result;
result = parse(sb);
outputobj[sb] = result;
result = parse(oth);
outputobj[oth] = result;

console.log(JSON.stringify(outputobj, null, '  '));

function parse(type){
    var returnVal = [];

    for (var i = 0; i < obj[type].length; i++) {
        var agency = obj[type][i];

        var name = agency[0];
        var link = agency[1];

        var newname = '';
        if(type != 'others'){
            newname = name.substring(name.indexOf('(')+1, name.length-1);
        }
        else{
            newname = name;
        }
        
        var newlink = url_toplevel + link;

        returnVal.push([newname, newlink]);
    }
    return returnVal;
}