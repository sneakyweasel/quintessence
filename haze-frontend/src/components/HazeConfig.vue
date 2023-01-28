<template>
    <div class="row">
        <div class="col">
            <h1>Enter places you might have been to:</h1>
            <hr>
        </div>
    </div>

    <form @submit.prevent="submit">
        <div v-for="i in 12" :key="'row' + i">
            <div class="row" :key="i">
                <div class="col-3"></div>
                <div class="col">
                    <input :id="'place' + i" type="text" class="form-control" :value="get_random_place()"
                        :key="'place' + i">
                </div>
                <div class="col">
                    <input :id="'prob' + i" type="range" class="form-range" value="0" min="0" max="100" step="10"
                        :key="'prob' + i">
                </div>
                <div class="col-3"></div>
            </div>
        </div>
        <hr>
        <hr>
        <button class="btn btn-outline-dark">
            Remember
        </button>
    </form>

    <div class="card-body">Returned bit string: {{ bitString }}</div>

</template>

<script>
import axios from "axios";

export default {
    props: {
    },
    data() {
        return {
            bitString: null
        };
    },
    methods: {
        get_random_place: function () {
            return places[Math.floor(Math.random() * places.length)];
        },
        submit: function () {
            // Simple POST request with a JSON body using axios
            let data = {
                places: [],
                probs: []
            };
            for (let i = 1; i < 10; i++) {
                const place = document.getElementById('place' + i).value;
                const prob = document.getElementById('prob' + i).value;
                data.places.push(place);
                data.probs.push(prob);
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
h1 {
    color: gray;
    margin-top: 0px;
    font-family: 'RoadRage', serif;
    font-size: 30px;
    text-shadow: 0 0 20px gray;
}

input[type="text"],
textarea {
    background-color: #151515;
    color: white;
    font-family: 'RoadRage', serif;
    font-size: 20px;
}

button {
    color: magenta;
    margin-top: 0px;
    font-family: 'RoadRage', serif;
    font-size: 40px;
    text-shadow: 0 0 20px magenta;
}
</style>
