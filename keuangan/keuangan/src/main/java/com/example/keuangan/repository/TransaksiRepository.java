package com.example.keuangan.repository;

import com.example.keuangan.entity.Transaksi;
import org.springframework.data.jpa.repository.JpaRepository;
import java.time.LocalDate;
import java.util.List;

public interface TransaksiRepository extends JpaRepository<Transaksi, Long> {
    List<Transaksi> findByTanggalBetween(LocalDate startDate, LocalDate endDate);
}

