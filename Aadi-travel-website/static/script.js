function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className==="topnav"){
        x.className += " responsive";
    }
    else {
        x.className = "topnav";
    }
}


document.addEventListener('DOMContentLoaded', function() {
  const startDateInput = document.getElementById('start-date');
  const endDateInput = document.getElementById('end-date');
  const numDaysSpan = document.getElementById('num-days');
  const roomTypeRadios = document.querySelectorAll('input[name="Rooms"]');
  const amountSpan = document.getElementById('amount');

  // Set min attribute for end date to be equal to start date
  startDateInput.addEventListener('change', function() {
    endDateInput.min = startDateInput.value;
  });

  // Set max attribute for start date to be equal to end date
  endDateInput.addEventListener('change', function() {
    startDateInput.max = endDateInput.value;
  });
  // Function to calculate the number of days between two dates
  function calculateNumberOfDays(startDate, endDate) {
    const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffDays = Math.round(Math.abs((end - start) / oneDay));
    return diffDays;
  }

  // Function to update the number of days
  function updateNumberOfDays() {
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;
    const numDays = calculateNumberOfDays(startDate, endDate);
    numDaysSpan.textContent = numDays;
  }

  function updateTotalAmount(){
    const selectedRoomtype = document.querySelector('input[name="Rooms"]:checked').value;
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;
    const numDays = calculateNumberOfDays(startDate, endDate);

    let ratePerDay = parseInt(selectedRoomtype);

    const totalAmount = ratePerDay * numDays;
    amountSpan.textContent = totalAmount;
  }

  // Event listeners for date inputs
  startDateInput.addEventListener('change', updateNumberOfDays);
  endDateInput.addEventListener('change', updateNumberOfDays);
  roomTypeRadios.forEach(radio => {
    radio.addEventListener('change', updateTotalAmount);
  });

  // Initial calculation of total amount
  updateTotalAmount();
});


                   
function updateNumberOfDays() {
  const startDate = startDateInput.value;
  const endDate = endDateInput.value;

  fetch('/calculate_days', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      start_date: startDate,
      end_date: endDate
    })
  })
  .then(response => response.json())
  .then(data => {
    numDaysSpan.textContent = data.num_days;
  })
  .catch(error => {
    console.error('Error:', error);
  });
}
                  

particlesJS("particles-js", {
    "particles": {
      "number": {
        "value": 33,
        "density": {
          "enable": true,
          "value_area": 1420.4657549380909
        }
      },
      "color": {
        "value": "#ffffff"
      },
      "shape": {
        "type": "triangle",
        "stroke": {
          "width": 0,
          "color": "#000000"
        },
        "polygon": {
          "nb_sides": 5
        },
        "image": {
          "src": "img/github.svg",
          "width": 100,
          "height": 100
        }
      },
      "opacity": {
        "value": 0.06313181133058181,
        "random": false,
        "anim": {
          "enable": false,
          "speed": 1,
          "opacity_min": 0.1,
          "sync": false
        }
      },
      "size": {
        "value": 11.83721462448409,
        "random": true,
        "anim": {
          "enable": false,
          "speed": 40,
          "size_min": 0.1,
          "sync": false
        }
      },
      "line_linked": {
        "enable": true,
        "distance": 150,
        "color": "#ffffff",
        "opacity": 0.4,
        "width": 1
      },
      "move": {
        "enable": true,
        "speed": 6,
        "direction": "none",
        "random": false,
        "straight": false,
        "out_mode": "out",
        "bounce": false,
        "attract": {
          "enable": false,
          "rotateX": 600,
          "rotateY": 1200
        }
      }
    },
    "interactivity": {
      "detect_on": "canvas",
      "events": {
        "onhover": {
          "enable": true,
          "mode": "repulse"
        },
        "onclick": {
          "enable": true,
          "mode": "push"
        },
        "resize": true
      },
      "modes": {
        "grab": {
          "distance": 400,
          "line_linked": {
            "opacity": 1
          }
        },
        "bubble": {
          "distance": 400,
          "size": 40,
          "duration": 2,
          "opacity": 8,
          "speed": 3
        },
        "repulse": {
          "distance": 200,
          "duration": 0.4
        },
        "push": {
          "particles_nb": 4
        },
        "remove": {
          "particles_nb": 2
        }
      }
    },
    "retina_detect": true
  });
   