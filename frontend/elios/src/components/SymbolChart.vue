<script>
export default {
    props: {
        symbol: String,
        indicators: String
    },  
}
</script>
<template>
    <div>Abount to render {{symbol}} symbol with {{indicators}} indicators</div>
</template>
<style scoped>
    .lw-chart {
        height: 100%;
    }
</style>