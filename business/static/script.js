var localityLimit = 20;
var localityOffset = 0;
var localityQuery = "";
var localityList = [];

var businessLimit = 12;
var businessOffset = 0;
var businessQuery = '';
var businessList = [];

// Function to get the locality list as paginated response //
const getLocalityList = (limit, offset, query) => {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4) {
        if (this.status === 200) {
          let response = JSON.parse(this.responseText);
          localityList = response['data'];
          localities = document.querySelector('#localities');
          localities.innerHTML = '';
          localitiesDataList = localityList.map((locality) => {
            var option = document.createElement('option');
            option.innerHTML = locality.locality;
            option.setAttribute('data-id', locality.id);
            localities.appendChild(option);
          })

        } else {
          var option = document.createElement('option');
          option.innerHTML = 'Could Not Load Data ...'
          option['data-value'] = 0;
          localities.appendChild(option);
        }
      }
    }
    // get locality list
    xhttp.open('get', `/localities?query=${query}&offset=${offset}&limit=${limit}`, true);
    xhttp.send();
}


// function to get paginated business list in response //
const getBusinessList = (limit, offset, locality, query) => {
    businessList = [];
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState === 4) {
        if (this.status === 200) {
          let response = JSON.parse(this.responseText);
          businessList = response['data'];
          var businessCardContainer = document.querySelector('#businessCardContainer');
          businessCardList = businessList.map((business) => {
            businessCardContainer.innerHTML += `
            <div class="card col-4 my-3 mx-3" style="width: 15rem;">
              <img src="https://afs.googleusercontent.com/yp/icon-100.png" class="card-img-top" alt="Business Icon">
              <div class="card-body">
                <h5 class="card-title">${business.name}</h5>
                <p class="card-text">
                    <a href="${business.website ? business.website : 'javascript:void(0)'}">website</a>
                </p>
                <h6 class="card-text">${business.phone}</h6>
                <p class="card-text">
                  <div>${business.street_address}</div>
                  <div>${business.locality}</div>
                </p>
              </div>
            </div>
            `;
          })
          businessOffset += businessLimit;
        } else {
          console.log('Cound not fetch Data');
        }
      }
    }
    // get locality list
    xhttp.open('get', `/search?query=${query}&locality=${locality}&offset=${offset}&limit=${limit}`, true);
    xhttp.send();
}

// get locality on typing in the input field //
const getLocalityListOnchange = (contextInput) => {
    if (contextInput.value.length >= 2) {
      getLocalityList(localityLimit, localityOffset, contextInput.value);
    }
}

// get business list on change of value in input //
const getBusinessListOnchange = (contextInput) => {
    localityQuery = contextInput.value;
    businessOffset = 0;
    document.querySelector('#businessCardContainer').innerHTML = '';
    getBusinessList(localityLimit, localityOffset, localityQuery, businessQuery);
}

// get business list on change of value in input //
const filterBusinessNamesOnchange = (contextInput) => {
    businessQuery = contextInput.value;
    localityQuery = document.querySelector('#localitySearchInput').value;
    businessOffset = 0;
    document.querySelector('#businessCardContainer').innerHTML = '';
    getBusinessList(businessLimit, businessOffset, localityQuery, businessQuery);
}

// function to load more businesses //
const loadMoreBusinesses = (contextBtn) => {
    localityQuery = document.querySelector('#localitySearchInput').value;
    getBusinessList(businessLimit, businessOffset, localityQuery, businessQuery);
}

// call locality initially
getLocalityList(localityLimit, localityOffset, localityQuery);

// clean the card container
document.querySelector('#businessCardContainer').innerHTML = '';
getBusinessList(businessLimit, businessOffset, localityQuery, '');