<template>
    <form @submit.prevent class="align-items-center">

        <!-- Quantum computer form card -->
        <div class="card mt-5">
            <div class="card-body">
                <h5 class="card-title">Quantum computer</h5>

                <!-- Quantum computer -->
                <div class="row mt-3">
                    <div class="col-5">
                        <label for="computer_select" class="form-label">
                            <span class="">Select quantum computer</span>
                        </label>
                    </div>
                    <div class="col-5">
                        <select id="computer_select" class="form-select" v-model="quantum_computer">
                            <option value="ionq" selected>IonQ</option>
                            <option value="ibmq">IBMQ 'simulator'</option>
                            <option value="pasqal">Pasqal 'simulator'</option>
                        </select>
                    </div>
                    <div class="col-2"></div>
                </div>

                <!-- Number of qbits -->
                <div class="row mt-3">
                    <div class="col-5">
                        <label for="qbit_count_range" class="form-label">
                            <span class="">Number of qbits:</span>
                        </label>
                    </div>
                    <div class="col-5">
                        <input id="qbit_count_range" v-model.number="qbit_count" type="range" class="form-range" min="2"
                            max="12" step="1" @input.prevent="change_qbit_count()">
                    </div>
                    <div class="col-2">
                        <span class="badge rounded-pill bg-primary">
                            {{ qbit_count }}
                        </span>
                    </div>
                </div>

                <!-- Trotter steps -->
                <div class="row mt-3">
                    <div class="col-5">
                        <label for="qbit_count_range" class="form-label">
                            <span class="">Number of steps:</span>
                        </label>
                    </div>
                    <div class="col-5">
                        <input id="steps_range" v-model.number="steps_count" type="range" class="form-range" min="2"
                            max="12" step="1">
                    </div>
                    <div class="col-2">
                        <span class="badge rounded-pill bg-primary">
                            {{ steps_count }}
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
                <div v-for="place, i in places" :key="'row' + i" class="row mt-2">

                    <!-- Place text input -->
                    <div class="col-5">
                        <div class="input-group">
                            <button class="btn btn-light" @click.prevent="update_place_input(i)">
                                🔄
                            </button>
                            <input :id="'place' + i" type="text" class="form-control" :value="place[0]" :key="'place' + i">
                        </div>
                    </div>
                    <!-- Probability slider input -->
                    <div class="col-5 mt-2">
                        <input :id="'prob' + i" type="range" class="form-range" :value="place[1]" min="0" max="100"
                            step="10" :key="'prob' + i" @input.prevent="update_percent_label(i)">
                    </div>
                    <!-- Probability percentage display -->
                    <div class="col-2 mt-1">
                        <span :id="'percent_label_' + i" class="badge rounded-pill bg-primary">
                            {{ place[1] }} %
                        </span>
                    </div>

                </div>
            </div>
        </div>

        <!-- Submit button -->
        <div class="row mt-4" v-if="!display_quantum_results">
            <div class="col-4"></div>
            <div class="col-4">
                <button id="submit_button" class="btn btn-lg w-100" type="submit" @click.prevent="submit_form">
                    Remember
                </button>
            </div>
            <div class="col-4"></div>
        </div>
    </form>

    <!-- Quantum circuit toggle -->
    <div class="card mt-4" v-if="display_quantum_results">
        <div class="card-body">
            <h5 class="card-title">Quantum computer results</h5>
            <p class="card-text">
                Here are the results from the quantum computer. The probability of each place is shown as a percentage.
            </p>

            <!-- Raw results -->
            <div class="bg-light">
                <p>
                    Raw quantum results: {{ raw_results }}
                </p>
                <p>
                    Error percentage: {{ (error_percentage * 100).toFixed(2) }} %
                </p>
                <p>
                    Entropy measure: {{ (entropy * 100).toFixed(2) }} % - {{ entropy_word }}
                </p>
            </div>

            <!-- Processed results -->
            <div v-for="[place, prob], i in results" :key="'qbit_result_' + i" class="row mt-2">

                <!-- Place text input -->
                <div class="col-5">
                    <div class="input-group">
                        <input :id="'result_place_' + i" type="text" class="form-control" :value="place"
                            :key="'result_place' + i" disabled>
                    </div>
                </div>
                <!-- Probability slider input -->
                <div class="col-5 mt-2">
                    <input :id="'result_prob' + i" type="range" class="form-range" :value="prob * 100" min="0" max="100"
                        step="10" :key="'result_prob' + i" disabled>
                </div>
                <!-- Probability percentage display -->
                <div class="col-2 mt-1">
                    <span :id="'percent_label_' + i" class="badge rounded-pill bg-primary">
                        {{ (prob * 100).toFixed(2) }} %
                    </span>
                </div>

            </div>
        </div>
    </div>

    <!-- AI toggle -->
    <div class="card mt-4" v-if="display_quantum_results">
        <div class="card-body">
            <h5 class="card-title">AI results</h5>
            <p class="card-text">
                Here are the generated prompt and the AI's response.
            </p>

            <!-- GPT3 prompt -->
            <div class="row mt-3">
                <p>
                    GPT3 prompt: {{ gpt3_prompt }}
                </p>
            </div>

            <!-- GPT3 response -->
            <div class="row mt-3">
                <p v-for="image_prompt, i in image_prompts" :key="'row' + i" class="row mt-2">
                    {{ image_prompt }}
                </p>
            </div>
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
            // Form
            qbit_count: 5,
            steps_count: 3,
            quantum_computer: 'ionq',
            places: [],
            // Quantum computer results
            results: [],
            raw_results: [],
            error_percentage: 0,
            entropy: 0,
            entropy_word: '',
            gpt3_prompt: '',
            gpt3_response: '',
            image_prompts: [],
            // UI
            display_quantum_results: false,
            display_ia: false,
            display_polar_plot: false,
            display_story: false,
        };
    },
    created() {
        for (let i = 0; i < this.qbit_count; i++) {
            this.places.push(this.create_new_place());
        }
        this.places[0][0] = 'Home';
    },
    methods: {
        get_random_place: function () {
            return DEFAULT_PLACES[Math.floor(Math.random() * DEFAULT_PLACES.length)];
        },
        get_random_value: function () {
            return Math.floor(Math.random() * 10) * 10;
        },
        create_new_place: function () {
            return [
                this.get_random_place(),
                this.get_random_value(),
            ];
        },
        change_qbit_count: function () {
            if (this.qbit_count < this.places.length) {
                this.places = this.places.slice(0, this.qbit_count);
            } else {
                for (let i = this.places.length; i < this.qbit_count; i++) {
                    this.places.push(this.create_new_place());
                }
            }
        },
        update_place_input: function (i) {
            const place = this.get_random_place();
            this.places[i][0] = place;
            document.getElementById('place' + i).value = place;
        },
        update_percent_label: function (i) {
            const percent = document.getElementById('prob' + i).value;
            document.getElementById('percent_label_' + i).innerHTML = percent + '%';
        },
        submit_form: function (event) {
            event.preventDefault();
            // Simple POST request with a JSON body using axios
            let data = {
                computer: this.quantum_computer,
                steps: this.steps_count,
                places: this.places,
            };

            const path = 'http://localhost:5000/generate';
            axios.post(path, data)
                .then(response => {
                    this.results = response.data.message.results;
                    this.raw_results = response.data.message.raw_results;
                    this.error_percentage = response.data.message.error_percentage;
                    this.entropy = response.data.message.entropy;
                    this.entropy_word = response.data.message.entropy_word;
                    this.gpt3_prompt = response.data.message.gpt3_prompt;
                    this.gpt3_response = response.data.message.gpt3_response;
                    this.image_prompts = response.data.message.image_prompts;
                    this.display_quantum_results = true;
                })
                .catch(err => {
                    alert('something went wrong! ' + err);
                })
        },
    }
}

const DEFAULT_PLACES = [
    "Rooftop bar",
    "Comedy club",
    "Concert venue",
    "Music festival",
    "Street fair",
    "Bowling alley",
    "Casino",
    "Sports stadium",
    "Karaoke bar",
    "Restaurant with live music",
    "Rooftop terrace",
    "Beach bonfire",
    "Drive-in movie theater",
    "Laser tag arena",
    "Trampoline park",
    "Escape room",
    "Miniature golf course",
    "Rock climbing gym",
    "Go-kart track",
    "Bowling alley",
    "Comedy club",
    "Concert hall",
    "Music festival",
    "Street festival",
    "Rooftop pool",
    "Rooftop garden",
    "Lounge",
    "Dance club",
    "Public square",
    "Rooftop yoga class"
];
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
