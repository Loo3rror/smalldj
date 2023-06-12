const manufDataBox = document.getElementById("cars-options");
const modelBox = document.getElementById("model-options");
const clientBox = document.getElementById("client-options");

const colorBox = document.getElementById("color-options");
const transBox = document.getElementById("trans-options");
const fuelBox = document.getElementById("fuel-options");

document.getElementById("loader").style.display = "none";

$.ajax({
  type: "GET",
  url: "manuf_data/",
  success: function (response) {
    const carManuf = response.car_data;
    carManuf.map((manuf) => {
      const option = document.createElement("option");
      option.textContent = manuf;
      option.setAttribute("class", "item");
      option.setAttribute("value", manuf);
      manufDataBox.appendChild(option);
    });
  },
  error: function (error) {
    console.log(error);
  },
});

manufDataBox.addEventListener("change", (event) => {
  modelBox.textContent = "";
  const activeManuf = event.target.value;
  $.ajax({
    type: "GET",
    url: "model_data/" + activeManuf + "/",
    success: function (response) {
      const carModel = response.model_data;
      carModel.map((model) => {
        const option = document.createElement("option");
        option.textContent = model;
        option.setAttribute("class", "item");
        option.setAttribute("value", model);
        modelBox.appendChild(option);
      });
    },
  });
});

const prd = [];
function addDict(item) {
  prd.push(item);
}

//get varinfo
const year_from = document.getElementById("year_from");
const year_to = document.getElementById("year_to");
const mileage_from = document.getElementById("mileage_from");
const mileage_to = document.getElementById("mileage_to");
const price_from = document.getElementById("price_from");
const price_to = document.getElementById("price_to");

const listButton = document.getElementById("generate_cars");

listButton.addEventListener("click", sendCars);

function sendCars() {
  var car = {
    client: clientBox.value,
    manuf: manufDataBox.value,
    model: modelBox.value,
    year_from: year_from.value,
    year_to: year_to.value,
    mileage_from: mileage_from.value,
    mileage_to: mileage_to.value,
    price_from: price_from.value,
    price_to: price_to.value,
    color: colorBox.value,
    fuel: fuelBox.value,
    transmission: transBox.value

  };
  console.log(car);
  document.getElementById("loader").style.display = "block";
  $.ajax({
    type: "POST",
    url: "read_car/",
    data: car,
    xhrFields: { responseType: "blob" },
    success: function (response) {
      var fileURL = window.URL.createObjectURL(response);
      var downloadLink = document.createElement("a");
      downloadLink.href = fileURL;
      downloadLink.download = manufDataBox.value + " " + modelBox.value+".xlsx";
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
      window.URL.revokeObjectURL(fileURL);
      document.getElementById("loader").style.display = "none";
    },
    error: function (xhr, status, error) {
      console.log("AJAX request failed:", status, error);
      document.getElementById("loader").style.display = "none";
    },
  });
}

function getParams(){
  $.ajax({
    type: "GET",
    url: "options_car/",
    success: function (response) {
      const paramsList = response.param_data;
      generateCarOptions(paramsList);
}})
}

function getFilters(){
  $.ajax({
    type: "GET",
    url: "filters_car/",
    success: function (response) {
      console.log(response);
      const colorsList = response.color_data;
      colorsList.map((color) => {
        const option = document.createElement("option");
        option.textContent = color.label;
        option.setAttribute("class", "item");
        option.setAttribute("value", color.value);
        colorBox.appendChild(option);
      });
      const transList = response.transm_data;
      transList.map((trans) => {
        const option = document.createElement("option");
        option.textContent = trans.label;
        option.setAttribute("class", "item");
        option.setAttribute("value", trans.value);
        transBox.appendChild(option);
      });
      const fuelList = response.fuel_data;
      fuelList.map((fuel) => {
        const option = document.createElement("option");
        option.textContent = fuel.label;
        option.setAttribute("class", "item");
        option.setAttribute("value", fuel.value);
        fuelBox.appendChild(option);
      });
}})
}



function generateCarOptions(data) {
  const wrapper = document.getElementById("car-options-wrapper");

  data.forEach((option) => {
    wrapper.insertAdjacentHTML(
      "beforeend",
      `  <div class="form-container__row mt-2">
    <input id="option_param" type="checkbox" name="options_param" value="${option.value}" />
    <label for="${option.id}">${option.label}</label>
  </div>`
    );
  });
}
 
getParams();
getFilters()