<template>
    <div class="container">
        <h1 id="title" class="text-center">Haze</h1>
        <h2 id="subtitle" class="text-center">Quantum comic strip generator</h2>
        <!-- <h2 id="subtitle" class="text-center">Quintessence - MIT iQuHACK 2023</h2> -->

        <div v-if="true">
            <HazeForm />
        </div>
        <div v-else>
            <HazeResults />
        </div>
</div>
</template>

<script>
import HazeForm from './components/HazeForm.vue'
import HazeResults from './components/HazeResults.vue'

export default {
    name: 'App',
    components: {
        HazeForm,
        HazeResults
    }
}
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
    /* color: #2c3e50; */

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
</style>
