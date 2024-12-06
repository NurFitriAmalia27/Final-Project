package com.example.keuangan.controller;

import com.example.keuangan.entity.Income;
import com.example.keuangan.entity.Transaksi;
import com.example.keuangan.repository.IncomeRepository;
import com.example.keuangan.repository.TransaksiRepository;
import com.example.keuangan.service.PredictionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@Controller
@RequestMapping("/transaksi")
public class TransaksiController {

    @Autowired
    private TransaksiRepository transaksiRepository;

    @Autowired
    private IncomeRepository incomeRepository;

    @Autowired
    private PredictionService predictionService;

    @GetMapping
    public String listTransaksiWithIncome(Model model) {
        List<Transaksi> transaksiList = transaksiRepository.findAll();
        model.addAttribute("transaksiList", transaksiList);

        LocalDate currentMonth = LocalDate.now().withDayOfMonth(1);
        Income currentIncome = incomeRepository.findByMonth(currentMonth);
        model.addAttribute("income", currentIncome != null ? currentIncome.getAmount() : 0.0);

        return "transaksi-list";
    }

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        int currentMonth = LocalDate.now().getMonthValue();
        Double prediction = predictionService.getPrediction(currentMonth);
        model.addAttribute("prediction", prediction);
        String chartUrl = "http://localhost:5000/chart";
        model.addAttribute("chartUrl", chartUrl);

        return "dashboard";
    }

    @PostMapping
    public String saveTransaksi(@ModelAttribute Transaksi transaksi) {
        transaksiRepository.save(transaksi);
        return "redirect:/transaksi";
    }
}
