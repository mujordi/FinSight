
function tab(id){
 document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
 document.getElementById(id).classList.add('active');
}

document.getElementById("state").innerText=DATA.macro.state;

const table=document.getElementById("macroTable");
table.innerHTML="<tr><th>Parameter</th><th>Value</th><th>Signal</th><th>Impact</th><th>Explanation</th></tr>"+
DATA.macro.parameters.map(p=>`<tr><td>${p.name}</td><td>${p.value}</td><td>${p.signal}</td><td>${p.impact}</td><td>${p.explanation}</td></tr>`).join("");

function chart(id,label,data,color){
 new Chart(document.getElementById(id),{
  type:"line",
  data:{labels:data.map((_,i)=>i),datasets:[{label:label,data:data,borderColor:color}]}
 });
}

chart("dxy","Dollar Index",DATA.series.dxy,"cyan");
chart("eur","EUR/USD",DATA.series.eurusd,"green");
chart("jpy","USD/JPY",DATA.series.usdjpy,"yellow");
chart("goldChart","Gold Price",DATA.series.gold,"gold");
chart("nasdaqChart","NASDAQ Composite",DATA.series.nasdaq,"cyan");
