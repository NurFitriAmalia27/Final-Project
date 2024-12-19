package com.example.keuangan.controller;

import com.example.keuangan.entity.Income;
import com.example.keuangan.entity.Transaksi;
import com.example.keuangan.repository.IncomeRepository;
import com.example.keuangan.repository.TransaksiRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.Month;
import java.util.*;
import java.util.stream.Collectors;

@Controller
@RequestMapping("/transaksi")
public class TransaksiController {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private TransaksiRepository transaksiRepository;

    @Autowired
    private IncomeRepository incomeRepository;

    @PostMapping("/setIncome")
    public String setIncome(@RequestParam("income") BigDecimal income) {
        LocalDate currentMonth = LocalDate.now().withDayOfMonth(1);
        Income existingIncome = incomeRepository.findByMonth(currentMonth);

        if (existingIncome == null) {
            Income newIncome = new Income();
            newIncome.setAmount(income.doubleValue());
            newIncome.setMonth(currentMonth);
            incomeRepository.save(newIncome);
        } else {
            existingIncome.setAmount(income.doubleValue());
            incomeRepository.save(existingIncome);
        }
        return "redirect:/transaksi";
    }

    @GetMapping
    public String listTransaksiWithIncome(Model model) {
        List<Transaksi> transaksiList = transaksiRepository.findAll();
        LocalDate currentMonth = LocalDate.now().withDayOfMonth(1);
        Income currentIncome = incomeRepository.findByMonth(currentMonth);

        model.addAttribute("transaksiList", transaksiList);
        model.addAttribute("income", currentIncome != null ? currentIncome.getAmount() : 0);
        return "transaksi-list";
    }

    @GetMapping("/edit/{id}")
    public String editTransaksi(@PathVariable Long id, Model model) {
        Transaksi transaksi = transaksiRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid transaksi ID: " + id));
        model.addAttribute("transaksi", transaksi);
        return "transaksi-edit";
    }

    @PostMapping("/update/{id}")
    public String updateTransaksi(@PathVariable Long id, @ModelAttribute Transaksi transaksi) {
        Transaksi existingTransaksi = transaksiRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid transaksi ID: " + id));
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
            List<Transaksi> transaksiList = transaksiRepository.findAll();
            LocalDate currentMonth = LocalDate.now().withDayOfMonth(1);
            Income currentIncome = incomeRepository.findByMonth(currentMonth);

            if (currentIncome == null) {
                model.addAttribute("error", "Pemasukan bulan ini belum diinput.");
                return "dashboard";
            }

            List<Integer> months = transaksiList.stream()
                    .map(transaksi -> transaksi.getTanggal().getMonthValue())
                    .toList();
            List<Double> expenses = transaksiList.stream()
                    .map(Transaksi::getJumlah)
                    .toList();
            double income = currentIncome.getAmount();

            String prediction = getPredictionFromFlask(months, expenses, income, model);

            model.addAttribute("prediction", prediction);
            model.addAttribute("totalIncome", income);
            model.addAttribute("totalExpenses", expenses.stream().mapToDouble(Double::doubleValue).sum());
        } catch (Exception e) {
            model.addAttribute("error", "Gagal mengambil data prediksi: " + e.getMessage());
        }

        return "dashboard";
    }

    private String getPredictionFromFlask(List<Integer> months, List<Double> expenses, double income, Model model) {
        String url = "http://localhost:5000/predict"; // Flask API endpoint
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("months", months);
        requestBody.put("expenses", expenses);
        requestBody.put("income", income);

        try {
            Map<String, Object> response = restTemplate.postForObject(url, requestBody, Map.class);
            String prediction = (String) response.get("prediction");
            String stdDev = (String) response.get("std_dev");

            model.addAttribute("std_dev", stdDev);
            return prediction;
        } catch (Exception e) {
            model.addAttribute("error", "Gagal memanggil Flask API: " + e.getMessage());
            return "Tidak dapat memprediksi data saat ini.";
        }
    }

    @GetMapping("/chart-data")
    @ResponseBody
    public Map<String, Object> getChartData() {
        List<Transaksi> transaksiList = transaksiRepository.findAll();

        // Pengeluaran per kategori
        Map<String, Double> categoryTotals = new HashMap<>();
        transaksiList.forEach(transaksi -> categoryTotals.merge(
                transaksi.getKategori(),
                transaksi.getJumlah(),
                Double::sum
        ));

        // Pengeluaran per bulan
        Map<Month, Double> monthlyTotals = transaksiList.stream()
                .collect(Collectors.groupingBy(
                        transaksi -> transaksi.getTanggal().getMonth(),
                        TreeMap::new, // Mengurutkan bulan secara kronologis
                        Collectors.summingDouble(Transaksi::getJumlah)
                ));

        List<String> months = monthlyTotals.keySet().stream()
                .map(Month::name)
                .toList();
        List<Double> monthlyAmounts = new ArrayList<>(monthlyTotals.values());

        Map<String, Object> response = new HashMap<>();
        response.put("categories", categoryTotals.keySet());
        response.put("amounts", categoryTotals.values());
        response.put("months", months);
        response.put("monthly_amounts", monthlyAmounts);

        return response;
    }
}
