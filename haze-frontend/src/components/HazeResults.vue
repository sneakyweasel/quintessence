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

        <div v-for="(step, index) in steps" :key="'step_div' + index">
            <div class="row">
                <h1>Step {{ index }}</h1>
            </div>
            <hr>
            <div class="row">
                <div class="col-1"></div>
                <div class="col-5">
                    <img class="img" :src="'../../../assets/pic' + index + '.png'" alt="" width="500px">
                </div>
                <div class="col-5">
                    <p class="steps">{{ step }}</p>

                </div>
                <div class="col-1"></div>
            </div>
            <hr>
            <hr>
        </div>

        <!-- <div class="row">
                <h1>Second step</h1>
            </div>
            <hr>
            <div class="row">
                <div class="col-1"></div>
                <div class="col-5">
                    <img class="img" src="../../../assets/pic1.png" alt="" width="500px">
                </div>
                <div class="col-5">
                    <p class="steps">
                        As he tried to piece together the events of the night, he remembered that he had been at the
                        concert
                        venue with some friends. They had been dancing and singing along to the music, and he had been
                        feeling incredibly alive. After the concert, they had decided to go to the rooftop bar to get a
                        drink and enjoy the view.
                    </p>
                </div>
                <div class="col-1"></div>
            </div>
            <hr>
            <hr> -->

        <!-- <div class="row">
                <h1>Third step</h1>
            </div>
            <hr>
            <div class="row">
                <div class="col-1"></div>
                <div class="col-5">
                    <img class="img" src="../../../assets/pic2.png" alt="" width="500px">
                </div>
                <div class="col-5">
                    <p class="steps">
                        Mr. Quanta remembered that the rooftop bar had been crowded, and he had been talking to some
                        people
                        he had just met. He remembered that they had been discussing philosophy and the meaning of life.
                        He
                        had been feeling inspired and energized by the conversation, and he had been enjoying himself
                        immensely. Suddenly, he had felt incredibly tired and had decided to take a nap. He had no idea
                        how
                        long he had been asleep, but he was glad to be back in the present moment.
                    </p>
                </div>
                <div class="col-1"></div>
            </div>
            <hr>
            <hr> -->

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
