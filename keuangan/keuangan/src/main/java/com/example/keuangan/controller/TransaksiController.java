package com.example.keuangan.controller;

import com.example.keuangan.entity.Transaksi;
import com.example.keuangan.repository.TransaksiRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

@Controller
@RequestMapping("/transaksi")
public class TransaksiController {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired  
    private TransaksiRepository transaksiRepository;

    private BigDecimal income;

    @PostMapping("/setIncome")
    public String setIncome(@RequestParam("income") BigDecimal income) {
        this.income = income;
        return "redirect:/transaksi";
    }

    @GetMapping
    public String listTransaksiWithIncome(Model model) {
        List<Transaksi> transaksiList = transaksiRepository.findAll();  
        model.addAttribute("transaksiList", transaksiList);
        model.addAttribute("income", income);
        return "transaksi-list";
    }

    @GetMapping("/edit/{id}")
    public String editTransaksi(@PathVariable Long id, Model model) {
        Transaksi transaksi = transaksiRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Invalid transaksi ID: " + id));
        model.addAttribute("transaksi", transaksi);
        return "transaksi-edit";
    }

    @PostMapping("/update/{id}")
    public String updateTransaksi(@PathVariable Long id, @ModelAttribute Transaksi transaksi) {
        Transaksi existingTransaksi = transaksiRepository.findById(id).orElseThrow(() -> new IllegalArgumentException("Invalid transaksi ID: " + id));
        existingTransaksi.setKategori(transaksi.getKategori());
        existingTransaksi.setJumlah(transaksi.getJumlah());
        existingTransaksi.setTanggal(transaksi.getTanggal());
        transaksiRepository.save(existingTransaksi);
        return "redirect:/transaksi";
    }

    @GetMapping("/delete/{id}")
    public String deleteTransaksi(@PathVariable Long id) {
        transaksiRepository.deleteById(id);
        return "redirect:/transaksi";
    }

    @PostMapping
    public String saveTransaksi(@ModelAttribute Transaksi transaksi) {
        transaksiRepository.save(transaksi);
        return "redirect:/transaksi";
    }

    @GetMapping("/dashboard")
    public String showDashboard(Model model) {
        try {
            // Ambil semua transaksi untuk dikirim ke Flask
            List<Transaksi> transaksiList = transaksiRepository.findAll();

            // Siapkan data untuk dikirim ke Flask
            List<Integer> months = transaksiList.stream()
                    .map(transaksi -> transaksi.getTanggal().getMonthValue())
                    .toList();
            List<Double> expenses = transaksiList.stream()
                    .map(Transaksi::getJumlah)
                    .toList();

            // Kirim data ke Flask untuk prediksi
            String prediction = getPredictionFromFlask(months, expenses);
            model.addAttribute("prediction", prediction);
        } catch (Exception e) {
            model.addAttribute("error", "Gagal mengambil data prediksi.");
        }

        return "dashboard";
    }

    private String getPredictionFromFlask(List<Integer> months, List<Double> expenses) {
        String url = "http://localhost:5000/predict";
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("months", months);
        requestBody.put("expenses", expenses);

        return restTemplate.postForObject(url, requestBody, String.class);
    }

    @GetMapping("/chart-data")
    @ResponseBody
    public Map<String, Object> getChartData() {
        List<Transaksi> transaksiList = transaksiRepository.findAll();

        // Proses data untuk grafik
        Map<String, Double> categoryTotals = new HashMap<>();
        transaksiList.forEach(transaksi -> categoryTotals.merge(
                transaksi.getKategori(),
                transaksi.getJumlah(),
                Double::sum
        ));

        Map<String, Object> response = new HashMap<>();
        response.put("categories", categoryTotals.keySet());
        response.put("amounts", categoryTotals.values());
        return response;
    }


}
