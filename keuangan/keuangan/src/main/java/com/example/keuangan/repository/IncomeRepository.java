package com.example.keuangan.repository;

import com.example.keuangan.entity.Income;
import org.springframework.data.jpa.repository.JpaRepository;

import java.time.LocalDate;

public interface IncomeRepository extends JpaRepository<Income, Long> {
    Income findByMonth(LocalDate month);
}
