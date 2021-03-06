#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _Gfluct_new_exc_reg(void);
extern void _Gfluct_new_inh_reg(void);
extern void _bg2pyr_reg(void);
extern void _bginh_reg(void);
extern void _ca_reg(void);
extern void _cadyn_reg(void);
extern void _cal2_reg(void);
extern void _cal2CA3_reg(void);
extern void _capool_reg(void);
extern void _capoolCA3_reg(void);
extern void _cas_reg(void);
extern void _cat_reg(void);
extern void _currentclamp_reg(void);
extern void _function_TMonitor_reg(void);
extern void _gap_reg(void);
extern void _h_reg(void);
extern void _hCA3_reg(void);
extern void _halfgap_reg(void);
extern void _im_reg(void);
extern void _imCA3_reg(void);
extern void _interD2interD_SOMPV_STFD_new_reg(void);
extern void _interD2interD_STFD_new_reg(void);
extern void _interD2pyrD_CR2P_STFD_new_reg(void);
extern void _interD2pyrD_SOM2P_STFD_new_reg(void);
extern void _interD2pyrD_STFD_new_reg(void);
extern void _kadist_reg(void);
extern void _kaprox_reg(void);
extern void _kca_reg(void);
extern void _kdrCA3_reg(void);
extern void _kdrca1_reg(void);
extern void _kdrca1DA_reg(void);
extern void _kdrinter_reg(void);
extern void _leak_reg(void);
extern void _leakCA3_reg(void);
extern void _leakDA_reg(void);
extern void _leakinter_reg(void);
extern void _na3_reg(void);
extern void _na3DA_reg(void);
extern void _nainter_reg(void);
extern void _nap_reg(void);
extern void _napCA3_reg(void);
extern void _nat_reg(void);
extern void _natCA3_reg(void);
extern void _pyrD2interD_P2CR_STFD_reg(void);
extern void _pyrD2interD_P2SOM_STFD_reg(void);
extern void _pyrD2interD_STFD_reg(void);
extern void _pyrD2pyrD_STFD_new_reg(void);
extern void _sahp_reg(void);
extern void _sahpCA3_reg(void);
extern void _sahpNE_reg(void);
extern void _vecevent_reg(void);
extern void _xtra_reg(void);
extern void _xtra_imemrec_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"Gfluct_new_exc.mod\"");
    fprintf(stderr," \"Gfluct_new_inh.mod\"");
    fprintf(stderr," \"bg2pyr.mod\"");
    fprintf(stderr," \"bginh.mod\"");
    fprintf(stderr," \"ca.mod\"");
    fprintf(stderr," \"cadyn.mod\"");
    fprintf(stderr," \"cal2.mod\"");
    fprintf(stderr," \"cal2CA3.mod\"");
    fprintf(stderr," \"capool.mod\"");
    fprintf(stderr," \"capoolCA3.mod\"");
    fprintf(stderr," \"cas.mod\"");
    fprintf(stderr," \"cat.mod\"");
    fprintf(stderr," \"currentclamp.mod\"");
    fprintf(stderr," \"function_TMonitor.mod\"");
    fprintf(stderr," \"gap.mod\"");
    fprintf(stderr," \"h.mod\"");
    fprintf(stderr," \"hCA3.mod\"");
    fprintf(stderr," \"halfgap.mod\"");
    fprintf(stderr," \"im.mod\"");
    fprintf(stderr," \"imCA3.mod\"");
    fprintf(stderr," \"interD2interD_SOMPV_STFD_new.mod\"");
    fprintf(stderr," \"interD2interD_STFD_new.mod\"");
    fprintf(stderr," \"interD2pyrD_CR2P_STFD_new.mod\"");
    fprintf(stderr," \"interD2pyrD_SOM2P_STFD_new.mod\"");
    fprintf(stderr," \"interD2pyrD_STFD_new.mod\"");
    fprintf(stderr," \"kadist.mod\"");
    fprintf(stderr," \"kaprox.mod\"");
    fprintf(stderr," \"kca.mod\"");
    fprintf(stderr," \"kdrCA3.mod\"");
    fprintf(stderr," \"kdrca1.mod\"");
    fprintf(stderr," \"kdrca1DA.mod\"");
    fprintf(stderr," \"kdrinter.mod\"");
    fprintf(stderr," \"leak.mod\"");
    fprintf(stderr," \"leakCA3.mod\"");
    fprintf(stderr," \"leakDA.mod\"");
    fprintf(stderr," \"leakinter.mod\"");
    fprintf(stderr," \"na3.mod\"");
    fprintf(stderr," \"na3DA.mod\"");
    fprintf(stderr," \"nainter.mod\"");
    fprintf(stderr," \"nap.mod\"");
    fprintf(stderr," \"napCA3.mod\"");
    fprintf(stderr," \"nat.mod\"");
    fprintf(stderr," \"natCA3.mod\"");
    fprintf(stderr," \"pyrD2interD_P2CR_STFD.mod\"");
    fprintf(stderr," \"pyrD2interD_P2SOM_STFD.mod\"");
    fprintf(stderr," \"pyrD2interD_STFD.mod\"");
    fprintf(stderr," \"pyrD2pyrD_STFD_new.mod\"");
    fprintf(stderr," \"sahp.mod\"");
    fprintf(stderr," \"sahpCA3.mod\"");
    fprintf(stderr," \"sahpNE.mod\"");
    fprintf(stderr," \"vecevent.mod\"");
    fprintf(stderr," \"xtra.mod\"");
    fprintf(stderr," \"xtra_imemrec.mod\"");
    fprintf(stderr, "\n");
  }
  _Gfluct_new_exc_reg();
  _Gfluct_new_inh_reg();
  _bg2pyr_reg();
  _bginh_reg();
  _ca_reg();
  _cadyn_reg();
  _cal2_reg();
  _cal2CA3_reg();
  _capool_reg();
  _capoolCA3_reg();
  _cas_reg();
  _cat_reg();
  _currentclamp_reg();
  _function_TMonitor_reg();
  _gap_reg();
  _h_reg();
  _hCA3_reg();
  _halfgap_reg();
  _im_reg();
  _imCA3_reg();
  _interD2interD_SOMPV_STFD_new_reg();
  _interD2interD_STFD_new_reg();
  _interD2pyrD_CR2P_STFD_new_reg();
  _interD2pyrD_SOM2P_STFD_new_reg();
  _interD2pyrD_STFD_new_reg();
  _kadist_reg();
  _kaprox_reg();
  _kca_reg();
  _kdrCA3_reg();
  _kdrca1_reg();
  _kdrca1DA_reg();
  _kdrinter_reg();
  _leak_reg();
  _leakCA3_reg();
  _leakDA_reg();
  _leakinter_reg();
  _na3_reg();
  _na3DA_reg();
  _nainter_reg();
  _nap_reg();
  _napCA3_reg();
  _nat_reg();
  _natCA3_reg();
  _pyrD2interD_P2CR_STFD_reg();
  _pyrD2interD_P2SOM_STFD_reg();
  _pyrD2interD_STFD_reg();
  _pyrD2pyrD_STFD_new_reg();
  _sahp_reg();
  _sahpCA3_reg();
  _sahpNE_reg();
  _vecevent_reg();
  _xtra_reg();
  _xtra_imemrec_reg();
}
