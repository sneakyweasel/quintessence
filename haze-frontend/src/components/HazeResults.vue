<template>
    <div class="row">
        <div class="col">
            <h1>Thanks to IonQ, we were able to retrace Mr Quanta's steps!</h1>
            <hr>
        </div>

        <div class="row">
            <div class="col-3"></div>
            <div class="col">
                <img class="img" src="../../../assets/roseplot.png" alt="" width="600px">
            </div>
            <div class="col-3"></div>
        </div>
        <hr>

        <div class="row">
            <h2>First step</h2>
        </div>
        <hr>
        <div class="row">
            <div class="col-1"></div>
            <div class="col-5">
                <img class="img" src="../../../assets/pic0.png" alt="" width="500px">
            </div>
            <div class="col-5">
                <p class="steps">
                    {{ steps[0] }}
                </p>
            </div>
            <div class="col-1"></div>
        </div>
        <hr>
        <hr>

        <div class="row">
            <h2>Second step</h2>
        </div>
        <hr>
        <div class="row">
            <div class="col-1"></div>
            <div class="col-5">
                <img class="img" src="../../../assets/pic1.png" alt="" width="500px">
            </div>
            <div class="col-5">
                <p class="steps">
                    {{ steps[1] }}
                </p>
            </div>
            <div class="col-1"></div>
        </div>
        <hr>
        <hr>

        <div class="row">
            <h2>Third step</h2>
        </div>
        <hr>
        <div class="row">
            <div class="col-1"></div>
            <div class="col-5">
                <img class="img" src="../../../assets/pic2.png" alt="" width="500px">
            </div>
            <div class="col-5">
                <p class="steps">
                    {{ steps[2] }}
                </p>
            </div>
            <div class="col-1"></div>
        </div>
        <hr>
        <hr>

    </div>
</template>

<script>
import json from '../../../assets/steps.json'
export default {
    name: 'HelloWorld',
    props: {
        msg: String
    },
    data() {
        return {
            steps: json
        }
    }
}
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

h2 {
    color: magenta;
    margin-top: 0px;
    font-family: 'RoadRage', serif;
    font-size: 30px;
    text-shadow: 0 0 20px magenta;
}

input[type="text"],
textarea {
    background-color: #151515;
    color: white;
    font-family: 'RoadRage', serif;
    font-size: 20px;
}

.steps {
    color: gray;
    margin-top: 0px;
    font-family: 'RoadRage', serif;
    font-size: 25px;
    text-shadow: 0 0 20px gray;
    vertical-align: middle;
}

button {
    color: magenta;
    margin-top: 0px;
    font-family: 'RoadRage', serif;
    font-size: 40px;
    text-shadow: 0 0 20px magenta;
}
</style>
