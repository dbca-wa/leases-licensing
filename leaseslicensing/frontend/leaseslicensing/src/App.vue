<template>
    <div id="app">
        <RouterView />
    </div>
</template>

<script>
import { RouterView } from 'vue-router';

export default {
    name: 'App',
    components: {
        RouterView,
    },
};
</script>

<style>
.popover {
    max-width: 100% !important;
}
.select2-container--disabled,
.select2-container--focus {
    z-index: 1;
}
</style>
