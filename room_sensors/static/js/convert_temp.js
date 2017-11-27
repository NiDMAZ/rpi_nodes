function convertTemp(val, cf) {
  if (cf == 'F') {return Math.round(5/9 * (val - 32));}
  if (cf == 'C') {return Math.round((val * 9/5) + 32);}
}

function getTempSign(cf) {
  if (cf == 'F') {return "C";}
  return "F";
}

$(document).ready(function(){
  $(".temp_list").click(function(){

var tempVal = document.getElementsByClassName("temp_val")[0].innerHTML;
var tempSign = document.getElementsByClassName("temp_sign")[0].innerHTML;
var newSign = getTempSign(tempSign);
var newVal = convertTemp(tempVal, tempSign);
document.getElementsByClassName("temp_val")[0].innerHTML = newVal;
document.getElementsByClassName("temp_sign")[0].innerHTML = newSign;

  });
});
