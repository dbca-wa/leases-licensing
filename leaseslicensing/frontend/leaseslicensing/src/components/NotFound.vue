<template>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-12 text-center">
                <h1>404</h1>
                <h2>Page Not Found</h2>
                <p class="lead">The page you are looking for does not exist.</p>
                <router-link to="/" class="btn btn-primary"
                    >Go Home</router-link
                >
            </div>
        </div>
    </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
h1 {
    font-size: 6rem;
    font-weight: bold;
    color: #6c757d;
}
h2 {
    margin-bottom: 1rem;
}
</style>
