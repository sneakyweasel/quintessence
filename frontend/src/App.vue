<template>
    <div class="container">
        <h1 id="title" class="text-center">Haze</h1>
        <h2 id="subtitle" class="text-center">Quantum comic strip generator</h2>
        <!-- <h2 id="subtitle" class="text-center">Quintessence - MIT iQuHACK 2023</h2> -->

        <form @submit.prevent class="align-items-center">

            <!-- Quantum computer form card -->
            <div class="card mt-5">
                <div class="card-body">
                    <h5 class="card-title">Quantum parameters</h5>
                    <p class="card-text">
                        Those parameters will change the way the quantum computer will generate the comic strip. Leave as
                        default if you don't know what you are doing.
                    </p>

                    <!-- Quantum computer -->
                    <div class="row mt-3">
                        <div class="col-5">
                            <label for="computer_select" class="form-label mt-1">
                                <span class="">Select quantum backend</span>
                            </label>
                        </div>
                        <div class="col-5">
                            <select id="computer_select" class="form-select" v-model="quantum_backend">
                                <option value="ibmq" selected>IBMQ simulator</option>
                                <option value="ionq">IonQ simulator</option>
                            </select>
                        </div>
                        <div class="col-2"></div>
                    </div>

                    <!-- Number of qbits -->
                    <div class="row mt-2">
                        <div class="col-5">
                            <label for="qbit_count_range" class="form-label">
                                <span class="">Number of qbits</span>
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
                    <div class="row mt-2">
                        <div class="col-5">
                            <label for="qbit_count_range" class="form-label">
                                <span class="">Number of trotter steps</span>
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

                    <!-- J values -->
                    <div class="row mt-2">
                        <div class="col-5">
                            <label for="jval_range" class="form-label">
                                <span class="">Quantum circuit J values</span>
                            </label>
                        </div>
                        <div class="col-5">
                            <input id="jval_range" v-model.number="jval" type="range" class="form-range" min="1" max="12"
                                step="1">
                        </div>
                        <div class="col-2">
                            <span class="badge rounded-pill bg-primary">
                                π / {{ jval }}
                            </span>
                        </div>
                    </div>

                    <!-- Toggle quantum simulator noise -->
                    <div class="row mt-2">
                        <div class="col-5">
                            <label for="qbit_count_range" class="form-label">
                                <span class="">Activate quantum noise</span>
                            </label>
                        </div>
                        <div class="col-5">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" v-model="activate_noise" id="noise_toggle">
                            </div>
                        </div>
                        <div class="col-2">
                        </div>
                    </div>

                    <!-- Toggle AI requests -->
                    <div class="row mt-2">
                        <div class="col-5">
                            <label for="qbit_count_range" class="form-label">
                                <span class="">Activate AI</span>
                            </label>
                        </div>
                        <div class="col-5">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" v-model="activate_ai" id="ai_toggle">
                            </div>
                        </div>
                        <div class="col-2">
                        </div>
                    </div>

                </div>
            </div>

            <!-- Storyline elements form card -->
            <div class="card mt-4">
                <div class="card-body">
                    <h5 class="card-title">Storyline elements</h5>
                    <p class="card-text">We are going to generate a short story using a random quantum walk generator from
                        your
                        starting position to various places you might have been to with varying chances.</p>
                    <p>
                        The first place will be your starting location.
                    </p>

                    <!-- Dynamic input - decrease index to start at 0 -->
                    <div v-for="place, i in places" :key="'row' + i" class="row mt-1">

                        <!-- Place text input -->
                        <div class="col-5">
                            <div class="input-group">
                                <button class="btn btn-light" @click.prevent="update_place_input(i)">
                                    🔄
                                </button>
                                <input :id="'place' + i" type="text" class="form-control" :value="place[0]"
                                    :key="'place' + i">
                            </div>
                        </div>
                        <!-- Probability slider input -->
                        <div class="col-4 mt-2">
                            <input :id="'prob' + i" type="range" class="form-range" :value="place[1]" min="0" max="100"
                                step="10" :key="'prob' + i" @input.prevent="update_percent_label(i)">
                        </div>

                        <!-- Probability raw value display -->
                        <div class="col-1 mt-1">
                            <span :id="'value_label_' + i" class="badge rounded-pill bg-primary">
                                {{ place[1] }}
                            </span>
                        </div>

                        <!-- Probability percentage display -->
                        <div class="col-1 mt-1">
                            <span :id="'percent_label_' + i" class="badge rounded-pill bg-secondary">
                                {{ place[2].toFixed(1) }} %
                            </span>

                        </div>

                    </div>
                </div>
                <Radar id="radar-chart" :options="chartOptions" :data="chartData" />
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


        <!-- Quantum circuit image display -->
        <div class="card mt-4" v-if="display_quantum_results">

            <div class="card-body">
                <h5 class="card-title">Quantum circuit</h5>
                <p class="card-text">
                    We generated a quantum circuit similar to the one below to simulate your quantum walk. The circuit is
                    made up of a sucession of trotter steps with the values you provided.
                </p>
                <img src="circuit.png" class="img-fluid">
            </div>
        </div>

        <!-- Quantum circuit toggle -->
        <div class="card mt-4" v-if="display_quantum_results">
            <div class="card-body">
                <h5 class="card-title">Quantum computer results</h5>
                <p class="card-text">
                    Here are the results from the quantum computer. The probability of each place is shown as a percentage.
                </p>

                <!-- Raw results -->
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <b>Raw results:</b> {{ raw_results }}
                    </li>
                    <li class="list-group-item">
                        <b>Error percentage:</b> {{ (error_percentage * 100).toFixed(2) }}%
                    </li>
                    <li class="list-group-item">
                        <b>Entropy measure:</b> {{ (entropy * 100).toFixed(2) }}% ({{ entropy_word }})
                    </li>
                </ul>

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
                            {{ (prob * 100).toFixed(2) }}%
                        </span>
                    </div>

                </div>
            </div>
        </div>

        <!-- GPT3 prompt -->
        <div class="card mt-4" v-if="display_quantum_results">
            <div class="card-body">
                <h5 class="card-title">AI prompt</h5>
                <p class="card-text">
                    We converted the quantum results to a prompt for GPT3 to generate a story.
                </p>
                <div class="row mt-3">
                    <p>
                        {{ gpt3_prompt }}
                    </p>
                </div>
            </div>
        </div>

        <!-- GPT3 response -->
        <div class="card mt-4" v-if="display_quantum_results && activate_ai">
            <div class="card-body">
                <h5 class="card-title">AI response</h5>
                <p class="card-text">
                    Here is the storyline generated by GPT3.
                </p>
                <div class="row mt-3">
                    <ul v-for="image_prompt, i in image_prompts" :key="'row' + i" class="list-group list-group-flush">
                        <li class="list-group-item">
                            {{ image_prompt }}
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <br>
        <br>
    </div>
</template>

<script>
import axios from "axios";
import { Radar } from 'vue-chartjs'
import { Chart as ChartJS, PolarAreaController, Filler, RadialLinearScale, PointElement, LineElement, ArcElement } from 'chart.js'

ChartJS.register(PolarAreaController, Filler, RadialLinearScale, PointElement, LineElement, ArcElement);


export default {
    components: { Radar },
    data() {
        return {
            // Form
            qbit_count: 5,
            steps_count: 4,
            jval: 6,
            quantum_backend: 'ibmq',
            places: [],
            activate_noise: true,
            activate_ai: false,
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
            // Chart
            chartOptions: {
                responsive: true,
                scale: {
                    r: {
                        min: 0,
                        // max: 100,
                        beginAtZero: true,
                        angleLines: {
                            display: false
                        },
                        ticks: {
                            display: false,
                            // stepSize: 10
                        },
                    }
                },
                elements: {
                    line: {
                        borderWidth: 4
                    }
                }
            }
        };
    },
    created() {
        for (let i = 0; i < this.qbit_count; i++) {
            this.places.push(this.create_new_place());
        }
        this.places[0][0] = 'Home';
    },
    mounted() {
        this.normalize_percentages();
    },
    computed: {
        chartData() {
            return {
                labels: this.places.map(p => p[0]),
                datasets: [{
                    label: 'Input Dataset',
                    data: this.places.map(p => p[2]),
                    fill: true,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgb(255, 99, 132)',
                    pointBackgroundColor: 'rgb(255, 99, 132)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(255, 99, 132)'
                }, {
                    label: 'Result Dataset',
                    data: this.results.map(p => p[1] * 100),
                    fill: true,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgb(54, 162, 235)',
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                }]
            };
        },
        total_probability() {
            let total = 0;
            for (let i = 0; i < this.places.length; i++) {
                const raw = this.places[i][1];
                total += raw;
            }
            return total;
        },
    },
    methods: {
        get_random_place: function () {
            return DEFAULT_PLACES[Math.floor(Math.random() * DEFAULT_PLACES.length)];
        },
        get_random_value: function () {
            return Math.floor(Math.random() * 10) * 10;
        },
        create_new_place: function () {
            let value = this.get_random_value();
            let percent = value / this.total_probability * 100;
            return [
                this.get_random_place(),
                value,
                percent
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
            this.chartData.labels = this.places.map(p => p[0]);
        },
        update_place_input: function (i) {
            const place = this.get_random_place();
            this.places[i][0] = place;
            document.getElementById('place' + i).value = place;
        },
        update_percent_label: function (i) {
            const raw_value = document.getElementById('prob' + i).value;
            this.places[i][1] = parseFloat(raw_value);
            this.normalize_percentages();
        },
        normalize_percentages() {
            let total = 0;
            for (let i = 0; i < this.places.length; i++) {
                const raw = this.places[i][1];
                total += raw;
            }
            for (let i = 0; i < this.places.length; i++) {
                const raw = this.places[i][1];
                const percent = raw / total * 100;
                this.places[i][2] = percent;
                document.getElementById('value_label_' + i).innerHTML = raw;
                document.getElementById('percent_label_' + i).innerHTML = percent + '%';
            }
        },
        submit_form: function (event) {
            event.preventDefault();
            // Simple POST request with a JSON body using axios
            let data = {
                quantum_backend: this.quantum_backend,
                steps: this.steps_count,
                jval: this.jval,
                places: this.places,
                activate_ai: this.activate_ai,
                activate_noise: this.activate_noise,
            };
            const path = 'http://localhost:8080/generate';
            axios.post(path, data)
                .then(response => {
                    this.results = response.data.message.results;
                    this.raw_results = response.data.message.raw_results;
                    this.ordered_results = response.data.message.ordered_results;
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

<style>
@font-face {
    font-family: "RoadRage";
    src: url("./assets/Road_Rage.otf");
}

#app,
html {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: #ccc;
}

#title {
    color: magenta;
    padding-top: 30px;
    margin-bottom: 0px;
    font-family: 'RoadRage', serif;
    font-size: 50px;
    text-shadow: 0 0 40px magenta;
}

#subtitle {
    color: #0808fe;
    margin-top: 0px;
    font-family: 'RoadRage', serif;
    font-size: 20px;
    text-shadow: 0 0 20px #0808fe;
}

#logo {
    padding-bottom: 100px;
}

a {
    font-size: 1.2rem;
    font-weight: bold;
    text-decoration: none;
    color: #2e3b48;
}

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
