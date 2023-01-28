<template>
    <div class="container">
        <h1 id="title">Quantum Haze</h1>
        <h2 id="subtitle">Quintessence - MIT iQuHACK 2023</h2>
        <img id="logo" alt="Vue logo" src="./assets/logo2.png" width="400">

        <HazeConfig />
    </div>
</template>

<script>
import HazeConfig from './components/HazeConfig.vue'

export default {
    name: 'App',
    components: {
        HazeConfig
    }
}
</script>

<style>
html {
    background-color: #16161d;
}

@font-face {
    font-family: "RoadRage";
    src: url("./assets/Road_Rage.otf");
}

#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    background-color: #000;
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
