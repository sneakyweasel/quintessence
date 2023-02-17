<template>
    <form @submit.prevent="" class="align-items-center">

        <!-- Quantum computer form card -->
        <div class="card mt-5">
            <div class="card-body">
                <h5 class="card-title">Quantum computer</h5>
                <div class="row mt-3"> <!-- Quantum computer -->
                    <div class="col-5">
                        <label for="computer_select" class="form-label">
                            <span class="">Select quantum computer</span>
                        </label>
                    </div>
                    <div class="col-5">
                        <select id="computer_select" class="form-select">
                            <option value="ionq" selected>IonQ</option>
                            <option value="ibmq">IBMQ 'simulator'</option>
                            <option value="pasqal">Pasqal 'simulator'</option>
                        </select>
                    </div>
                    <div class="col-2"></div>
                </div>

                <div class="row mt-3"> <!-- Number of qbits -->
                    <div class="col-5">
                        <label for="qbit_count_range" class="form-label">
                            <span class="">Number of qbits:</span>
                        </label>
                    </div>
                    <div class="col-5">
                        <input id="qbit_count_range" v-model.number="qbit_count" type="range" class="form-range" min="2"
                            max="12" step="1" @input="update_all_percent_labels()">
                    </div>
                    <div class="col-2">
                        <span class="badge rounded-pill bg-primary">
                            {{ qbit_count }}
                        </span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Storyline elements form card -->
        <div class="card mt-4">
            <div class="card-body">
                <h5 class="card-title">Storyline elements</h5>
                <p class="card-text">We are going to generate a short story using a random quantum walk generator from your
                    starting position to various places you might have been to with varying chances.</p>
                <p>
                    The first place will be your starting location.
                </p>

                <!-- Dynamic input - decrease index to start at 0 -->
                <div v-for="i in qbit_count" :key="'row' + (i - 1)" class="row mt-2">

                    <!-- Place text input -->
                    <div class="col-5">
                        <div class="input-group">
                            <button class="btn btn-light" @click.prevent="update_place_input(i - 1)">
                                🔄
                            </button>
                            <input :id="'place' + (i - 1)" type="text" class="form-control" :value="get_random_place()"
                                :key="'place' + (i - 1)">
                        </div>
                    </div>
                    <!-- Probability slider input -->
                    <div class="col-5 mt-2">
                        <input :id="'prob' + (i - 1)" type="range" class="form-range" :value="get_random_value()" min="0"
                            max="100" step="10" :key="'prob' + (i - 1)" @input="update_percent_label(i - 1)">
                    </div>
                    <!-- Probability percentage display -->
                    <div class="col-2 mt-1">
                        <span :id="'percent_label_' + (i - 1)" class="badge rounded-pill bg-primary">
                            0 %
                        </span>
                    </div>

                </div>
            </div>
        </div>

        <!-- Submit button -->
        <div class="row mt-4" v-if="!display_quantum_circuit">
            <div class="col-4"></div>
            <div class="col-4">
                <button id="submit_button" class="btn btn-lg" @click="submit_query">
                    Remember
                </button>
            </div>
            <div class="col-4"></div>
        </div>
    </form>

    <!-- Quantum circuit toggle -->
    <div class="card mt-4" v-if="display_quantum_circuit">
        <div class="card-body">
            <h5 class="card-title">Quantum computer response</h5>
            <p class="card-text">
                The quantum computer has been asked to generate a random quantum walk from your input parameters.
            </p>
            <p>{{ response }}</p>
        </div>
    </div>
    <br>
<br>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            qbit_count: 5,
            display_quantum_circuit: false,
            display_polar_plot: false,
            display_story: false,
            response: null,
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
        update_place_input: function (i) {
            const place = this.get_random_place();
            document.getElementById('place' + i).value = place;
        },
        update_percent_label: function (i) {
            const percent = document.getElementById('prob' + i).value;
            document.getElementById('percent_label_' + i).innerHTML = percent + '%';
        },
        update_all_percent_labels: function () {
            for (let i = 0; i < this.qbit_count; i++) {
                this.update_percent_label(i);
            }
        },
        submit_query: function () {
            // Simple POST request with a JSON body using axios
            let data = {
                computer: document.getElementById('computer_select').value,
                qbit_count: this.qbit_count,
                places: [],
            };
            for (let i = 0; i < this.qbit_count; i++) {
                const place = document.getElementById('place' + i).value;
                const prob_str = document.getElementById('prob' + i).value;
                const probability = parseFloat(prob_str) / 100;
                data.places.push({ place, probability });
            }
            console.log(data);

            const path = 'http://localhost:5000/generate';
            axios.post(path, data)
                .then(res => {
                    this.response = res.data;
                    this.display_quantum_circuit = true;
                })
                .catch(err => {
                    alert('something went wrong! ' + err);
                })
        }
    },
    mounted() {
        for (let i = 0; i < this.qbit_count; i++) {
            this.update_percent_label(i);
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

#submit_button {
    color: magenta;
    margin-top: 0px;
    font-family: 'RoadRage', serif;
    font-size: 30px;
    text-shadow: 0 0 20px magenta;
    background-color: white;
}
</style>
