package com.example.keuangan.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class PredictionService {

    private final String flaskApiUrl = "http://localhost:5000/predict";

    public Double getPrediction(int month) {
        try {
            String requestUrl = flaskApiUrl + "?month=" + month;

            RestTemplate restTemplate = new RestTemplate();
            PredictionResponse response = restTemplate.getForObject(requestUrl, PredictionResponse.class);

            if (response != null && "success".equalsIgnoreCase(response.getStatus())) {
                return response.getPrediction();
            }
        } catch (Exception e) {
            System.out.println("Error saat melakukan prediksi: " + e.getMessage());
        }
        return null;
    }

    public static class PredictionResponse {
        private String status;
        private Double prediction;

        public String getStatus() {
            return status;
        }

        public void setStatus(String status) {
            this.status = status;
        }

        public Double getPrediction() {
            return prediction;
        }

        public void setPrediction(Double prediction) {
            this.prediction = prediction;
        }
    }
}
