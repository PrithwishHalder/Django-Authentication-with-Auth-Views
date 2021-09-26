function medal(data1, data2, data3, data4) {
  options = {
    series: [
      { name: "Gold", type: "line", data: data1 },
      { name: "Silver", type: "line", data: data2 },
      { name: "Bronze", type: "line", data: data3 },
    ],
    chart: { height: 378, type: "line", offsetY: 10 },
    stroke: { width: [2, 3] },
    plotOptions: { bar: { columnWidth: "50%" } },
    colors: colors,
    dataLabels: { enabled: !0, enabledOnSeries: [1] },
    labels: data4,
    xaxis: { type: "datetime" },
    legend: { offsetY: 7 },
    grid: { padding: { bottom: 20 } },
    fill: { type: "gradient", gradient: { shade: "light", type: "horizontal", shadeIntensity: 0.25, gradientToColors: void 0, inverseColors: !0, opacityFrom: 0.75, opacityTo: 0.75, stops: [0, 0, 0] } },
    yaxis: [{ title: { text: "Medal Count" } }],
  };
  (chart = new ApexCharts(document.querySelector("#medal"), options)).render();
}
