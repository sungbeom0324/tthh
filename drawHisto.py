import ROOT
import numpy as np
ROOT.gStyle.SetOptStat(0)

tthh   = "./samples/tthh.root"
ttbbbb = "./samples/ttbbbb.root"
ttbbcc = "./samples/ttbbcc.root"
ttbb   = "./samples/ttbb.root"
TreeName = "Delphes"

# RDF
tthh   = ROOT.RDataFrame(TreeName, tthh)
ttbbbb = ROOT.RDataFrame(TreeName, ttbbbb)
ttbbcc = ROOT.RDataFrame(TreeName, ttbbcc)
ttbb   = ROOT.RDataFrame(TreeName, ttbb)
dfs = {"tthh": tthh, "ttbbbb": ttbbbb, "ttbbcc": ttbbcc, "ttbb": ttbb }

def drawHisto(hists, dfs, flag="_S0"):
    canvas = ROOT.TCanvas("c", "c", 400, 400)
    for hist_name in hists:
        hist_dict = {}
        legend = ROOT.TLegend(0.75, 0.75, 0.85, 0.85)

        ymax, color = 0, 1
        for df_name, df in dfs.items():
            nbin, xmin, xmax = 20, 0, 400
            if df.Max(hist_name).GetValue() < 100: xmax = 100
            if df.Max(hist_name).GetValue() < 20: nbin, xmax = 12, 12
            if df.Min(hist_name).GetValue() < 0: nbin, xmin, xmax = 20, -4, 4
            h = df.Histo1D(ROOT.RDF.TH1DModel(hist_name, hist_name, nbin, xmin, xmax), hist_name)
            if ymax < h.GetMaximum(): ymax = h.GetMaximum()
            h.GetXaxis().SetTitle(hist_name)
            h.GetYaxis().SetTitle("a.u.")
            h.SetLineColor(color)
            color+=1
            h.SetLineWidth(2)
            legend.AddEntry(h.GetValue(), df_name, "l")
            hist_dict[hist_name + "_" + df_name] = h

        first = True
        for _tmp, h in hist_dict.items():
            if first:
                h.SetMaximum(ymax + 0.2)
                h.DrawNormalized("hist")
                first = False
            else: h.DrawNormalized("same")
        legend.Draw()
        canvas.Print("./plots/" + hist_name + flag + ".pdf")
        canvas.Clear()

## Histogram Features  
hists_S0 = [
        "Muon_size", "Electron_size", "Jet_size",
        "nGenAddQuark", "nGenAddbQuark", "nGenAddcQuark",
        "nGenAddJet", "nGenAddbJet", "nGenAddcJet", "nGenAddlfJet", "nLepFromTop",
]

hists_S1 = hists_S0 + [
        "Electron1_pt",
]

hists_S2 = hists_S1 + [
        "Jet1_pt", "Jet2_pt", "Jet3_pt", "Jet4_pt", "Jet5_pt",
]

hists_S3 = hists_S2 + [
        "bJet1_pt", "bJet2_pt", "bJet3_pt",
]

# nocut
drawHisto(hists_S0, dfs, "_S0")

# cut1. nLepton selection
for dfname, df in dfs.items():
    df = df.Filter("Electron_size==1") \
           .Define("Electron1_pt", "Electron_pt[0]")
    dfs[dfname] = df
drawHisto(hists_S1, dfs, "_S1")

# cut2. nJet selection
for dfname, df in dfs.items():
    df = df.Filter("Jet_size>=5") \
           .Define("Jet1_pt", "Jet_pt[0]") \
           .Define("Jet2_pt", "Jet_pt[1]") \
           .Define("Jet3_pt", "Jet_pt[2]") \
           .Define("Jet4_pt", "Jet_pt[3]") \
           .Define("Jet5_pt", "Jet_pt[4]")
    dfs[dfname] = df
drawHisto(hists_S2, dfs, "_S2")

# cut3. nbJet selection
for dfname, df in dfs.items():
    df = df.Filter("bJet_size>=3") \
           .Define("bJet1_pt", "bJet_pt[0]") \
           .Define("bJet2_pt", "bJet_pt[1]") \
           .Define("bJet3_pt", "bJet_pt[2]")
    dfs[dfname] = df
drawHisto(hists_S3, dfs, "_S3")

