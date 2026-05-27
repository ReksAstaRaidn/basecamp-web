import graphviz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os   

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        
        #posisi untuk visualisasi dengan graphviz (x, y)
        self.posisi = {
            "Basecamp": "0, 0!",
            "Pos 1": "-1.2, 2.5!",
            "Pos 2": "1.2, 5.0!",
            "Pos 3": "-1.2, 7.5!",
            "Puncak": "0, 10.0!"
        }
        
    # tambah pos baru ke dalam graph
    def tambah_pos(self, pos):
        if pos not in self.adjacency_list:
            self.adjacency_list[pos] = []
            
    
    #tambah jalur antara dua pos dengan jarak tertentu
    def tambah_jalur(self, pos1, pos2, jarak):
        if pos1 in self.adjacency_list and pos2 in self.adjacency_list:
            self.adjacency_list[pos1].append({"ke": pos2, "jarak": jarak})
            self.adjacency_list[pos2].append({"ke": pos1, "jarak": jarak})
    
    #tampilkan jalur dengan format yang lebih rapi
    def show_jalur(self):
        print("\nJalur Pendakian:")
        #tampilkan jalur dengan format yang lebih rapi
        for pos, jalur in self.adjacency_list.items():
            koneksi = ", ".join([f"{j['ke']} (jarak: {j['jarak']} MDPL)" for j in jalur])
            print(f"[{pos}] terhubung ke: {koneksi if koneksi else 'Tidak ada jalur'}")
    
    #visualisasikan jalur pendakian dengan graphviz dan matplotlib
    def visualisasi_jalur(self):
        print("\nVisualisasi Jalur Pendakian:")
        #buat graph tak berarah dengan graphviz
        dot = graphviz.Digraph('Peta_Pendakian', comment='Jalur Pendakian', engine='neato')
        dot.attr(size='8,11')
        
        #atur gaya node dan edge 
        dot.attr('node', shape='ellipse', style='filled', color='darkgreen', fontcolor='white', fontsize='11', width='1.2', height='0.6', fontname='Helvetica')
        dot.attr('edge', color='gray', style='dashed', fontcolor='red', fontname='Helvetica', fontsize='16', arrowsize='0.7')
        
        #tambahkan node dengan posisi yang sudah ditentukan
        for pos in self.adjacency_list.keys():
            if pos in self.posisi:
                dot.node(pos, pos, pos=self.posisi[pos])
            else:
                dot.node(pos, pos)
        
        #tambahkan edge dengan label jarak dan pastikan tidak menggambar edge ganda
        drawn_edges = set()
        
        #iterasi semua jalur untuk menambahkan edge ke graph
        for pos, jalur in self.adjacency_list.items():
            for j in jalur:
                target = j['ke']
                jarak = j['jarak']
                
                #buat edge dengan urutan yang konsisten untuk menghindari duplikasi
                edge = tuple(sorted([pos, target]))
                if edge not in drawn_edges:
                    dot.edge(pos, target, label=f"{jarak} MDPL")
                    drawn_edges.add(edge)
        
        #render graph ke file sementara dan tampilkan dengan matplotlib        
        try:
            filename = 'jalur_pendakian'
            dot.render(filename, format='png', view=False, cleanup=True)
            
            
            img_path = f"{filename}.png"
            img = mpimg.imread(img_path)
            
            # tampilkan gambar dengan matplotlib
            fig, ax = plt.subplots(figsize=(7, 9))
            ax.imshow(img)
            ax.axis('off')
            
            plt.title("Peta Jalur Pendakian", fontsize=16, fontweight='bold', pad=20)
            
            # Koordinat pusat kompas (relatif 0.0 - 1.0 terhadap area chart)
            kompas_x, kompas_y = 0.85, 0.80 
            r = 0.035  # Panjang jarum/panah
            d = 0.055  # Jarak teks dari titik pusat (membuatnya renggang)
            
            # Fungsi pembantu untuk menggambar tanda panah arah
            def gambar_panah(x_ke, y_ke, warna='black'):
                ax.annotate('', xy=(x_ke, y_ke), xytext=(kompas_x, kompas_y),
                            xycoords='axes fraction', textcoords='axes fraction',
                            arrowprops=dict(facecolor=warna, width=1.2, headwidth=6, headlength=7, edgecolor=warna))

            # Gambar empat arah panah (Utara diberi warna merah sebagai penanda utama)
            gambar_panah(kompas_x, kompas_y + r, warna='red')     # Utara (Atas)
            gambar_panah(kompas_x, kompas_y - r, warna='black')   # Selatan (Bawah)
            gambar_panah(kompas_x + r, kompas_y, warna='black')   # Timur (Kanan)
            gambar_panah(kompas_x - r, kompas_y, warna='black')   # Barat (Kiri)

            # Tambahkan label huruf di ujung luar panah agar tidak menumpuk
            ax.text(kompas_x, kompas_y + d, 'U', transform=ax.transAxes, ha='center', va='center', fontsize=11, fontweight='bold', color='red')
            ax.text(kompas_x, kompas_y - d, 'S', transform=ax.transAxes, ha='center', va='center', fontsize=11, fontweight='bold', color='black')
            ax.text(kompas_x + d, kompas_y, 'T', transform=ax.transAxes, ha='center', va='center', fontsize=11, fontweight='bold', color='black')
            ax.text(kompas_x - d, kompas_y, 'B', transform=ax.transAxes, ha='center', va='center', fontsize=11, fontweight='bold', color='black')

            # Titik pusat lingkaran kecil kompas
            ax.plot(kompas_x, kompas_y, marker='o', color='black', markersize=3, transform=ax.transAxes)
            
            plt.tight_layout()
            plt.show()
            
            if os.path.exists(img_path):
                os.remove(img_path)
            
        except Exception as e:
            print(f"Gagal membuat visualisasi jalur pendakian: {e}")