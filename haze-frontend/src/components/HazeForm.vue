<template>
    <div class="card mt-5">
        <div class="card-body">
            <h5 class="card-title">Quantum computer</h5>
            <div class="row mt-3"> <!-- Quantum computer -->
                <div class="col-6">
                    <label for="computer_select" class="form-label">
                        <span class="">Select quantum computer</span>
                    </label>
                </div>
                <div class="col-6">
                    <select id="computer_select" class="form-select">
                        <option value="ionq" selected>IonQ</option>
                        <option value="ibmq">IBMQ 'simulator'</option>
                        <option value="pasqal">Pasqal 'simulator'</option>
                    </select>
                </div>
            </div>

            <div class="row mt-3"> <!-- Number of qbits -->
                <div class="col-6">
                    <label for="qbit_count_range" class="form-label">
                        <span class="">Number of qbits: <b>{{ qbit_count }}</b></span>
                    </label>
                </div>
                <div class="col-6">
                    <input id="qbit_count_range" v-model.number="qbit_count" type="range" class="form-range" min="2"
                        max="12" step="1">
                </div>
            </div>
        </div>
    </div>

    <div class="card mt-4">
        <div class="card-body">
            <h5 class="card-title">Storyline elements</h5>
            <p class="card-text">We are going to generate a story using a random quantum walk generator from your starting
                position to various places you might have been to with varying chances.</p>
            <p>
                The first place will be your starting location.
            </p>

            <form @submit.prevent="submit" class="align-items-center">

                <!-- Dynamic input -->
                <div v-for="i in qbit_count" :key="'row' + i" class="mt-2">
                    <div class="row" :key="i">
                        <!-- Place text input -->
                        <div class="col-6">
                            <input :id="'place' + i" type="text" class="form-control" :value="get_random_place()"
                                :key="'place' + i">
                        </div>
                        <!-- Probability slider input -->
                        <div class="col-5 mt-2">
                            <input :id="'prob' + i" type="range" class="form-range" :value="get_random_value()" min="0"
                                max="100" step="10" :key="'prob' + i" @input="update_percent_label(i)">
                        </div>
                        <!-- Probability percentage display -->
                        <div class="col-1 mt-1">
                            <span :id="'percent_label_' + i">0%</span>
                        </div>
                    </div>
                </div>

            </form>
        </div>
    </div>

    <div class="row mt-4">
        <div class="col-4"></div>
        <div class="col-4">
            <button class="btn btn-lg">
                Remember
            </button>
        </div>
        <div class="col-4"></div>
</div>
</template>

<script>






import axios from "axios";

export default {
    data() {
        return {
            qbit_count: 5,
            bitString: null
        };
    },
    methods: {
        get_random_place: function () {
            return places[Math.floor(Math.random() * places.length)];
            // return places.pop();
        },
        get_random_value: function () {
            return Math.floor(Math.random() * 100);
        },
        update_percent_label: function (i) {
            const percent = document.getElementById('prob' + i).value;
            document.getElementById('percent_label_' + i).innerHTML = percent + '%';
        },
        submit: function () {
            // Simple POST request with a JSON body using axios
            let data = {
                places: [],
            };
            for (let i = 1; i < 10; i++) {
                const place = document.getElementById('place' + i).value;
                const probability = document.getElementById('prob' + i).value;
                data.places.push({ place, probability });
            }
            console.log(data);

            axios.post('/api', data)
                .then(res => {
                    this.bitString = res.data.bitString;
                })
                .catch(err => {
                    alert('something went wrong! ' + err);
                })
        }
    }
}

var places = [
    "A rooftop bar",
    "A comedy club",
    "A concert venue",
    "A music festival",
    "A street fair",
    "A bowling alley",
    "A casino",
    "A sports stadium",
    "A karaoke bar",
    "A restaurant with live music",
    "A rooftop terrace",
    "A beach bonfire",
    "A drive-in movie theater",
    "A laser tag arena",
    "A trampoline park",
    "An escape room",
    "A miniature golf course",
    "A rock climbing gym",
    "A go-kart track",
    "A bowling alley",
    "A comedy club",
    "A concert hall",
    "A music festival",
    "A street festival",
    "A rooftop pool",
    "A rooftop garden",
    "A lounge",
    "A dance club",
    "A public square",
    "A rooftop yoga class"];

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
input[type="range"]::-moz-range-progress {
    background-color: magenta;
}

input[type="range"]::-moz-range-track {
    background-color: grey;
}

input[type="range"]::-ms-fill-lower {
    background-color: magenta;
}

input[type="range"]::-ms-fill-upper {
    background-color: grey;
}

button {
    color: magenta;
    margin-top: 0px;
    font-family: 'RoadRage', serif;
    font-size: 30px;
    text-shadow: 0 0 20px magenta;
    background-color: white;
}
</style>
