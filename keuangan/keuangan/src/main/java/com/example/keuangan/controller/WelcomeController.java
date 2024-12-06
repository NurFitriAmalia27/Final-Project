package com.example.keuangan.controller;

import com.example.keuangan.entity.Income;
import com.example.keuangan.repository.IncomeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;

@Controller
@RequestMapping("/")
public class WelcomeController {

    @Autowired
    private IncomeRepository incomeRepository;

    @GetMapping
    public String welcome() {
        return "welcome";
    }

    @PostMapping("/saveIncome")
    public String saveIncome(@RequestParam Double income) {
        LocalDate currentMonth = LocalDate.now().withDayOfMonth(1);
        Income existingIncome = incomeRepository.findByMonth(currentMonth);

        if (existingIncome == null) {
            Income newIncome = new Income();
            newIncome.setAmount(income);
            newIncome.setMonth(currentMonth);
            incomeRepository.save(newIncome);
        } else {
            existingIncome.setAmount(income);
            incomeRepository.save(existingIncome);
        }

        return "redirect:/transaksi";
    }
}
