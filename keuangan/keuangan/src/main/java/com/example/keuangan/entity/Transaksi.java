package com.example.keuangan.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
public class Transaksi {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String kategori;
    private Double jumlah;
    private LocalDate tanggal;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getKategori() { return kategori; }
    public void setKategori(String kategori) { this.kategori = kategori; }

    public Double getJumlah() { return jumlah; }
    public void setJumlah(Double jumlah) { this.jumlah = jumlah; }

    public LocalDate getTanggal() { return tanggal; }
    public void setTanggal(LocalDate tanggal) { this.tanggal = tanggal; }
}

