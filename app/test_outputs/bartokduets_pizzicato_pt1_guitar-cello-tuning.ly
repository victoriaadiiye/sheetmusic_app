
    \version "2.24.0"
    \makeDefaultStringTuning #'guitar-cello-tuning \stringTuning <c, g, d g a e'>
    \paper {
        indent = 0
        ragged-bottom = ##f
        ragged-last-bottom = ##f
        ragged-last = ##f
        ragged-right = ##f
    }

    \layout {
    \context {
        \Score
    }
    \context {
        \Staff
    }
    }
    #(define (systemPair music)
    #{

        \new StaffGroup <<
            \new Staff { \clef "treble_8" \time 3/2 \key g \major #music }
            \new TabStaff \with { stringTunings = #guitar-cello-tuning }
            { \clef "moderntab" \time 3/2 \key g \major #music }
        >>
    #})







mA = { b,8 d8 cis8 d8 e4 d4 c4 b,4 | g,8 b,8 a,8 b,8 c4 b,4 a,4 g,4 | g,8 b,8 a,8 b,8 c4 b,4 e4 d4 | g,8 b,8 a,8 b,8 c4 b,4 a,4 <g, d> 4 | }
\score { #(systemPair mA) }

        mB = { r2 g,8 a,8 b,8 cis8 d8 e8 f8 gis8 | a4 r4 b8 cis'8 dis'8 e'8 f'8 gis'8 ais'8 b'8 | f'4 r4 g,8 gis,8 ais,8 b,8 cis8 d8 e8 f8 | gis4 r4 r8 g,8 gis,8 ais,8 b,8 cis8 d8 b,8 | }
        \score { #(systemPair mB) }

        mC = { a,4 r4 r4 <gis, fis> 4 r4 <gis, fis> 4 | r4 <gis, fis> 4 r4 <gis, f> 4 r4 <gis, f> 4 | r4 <gis, f> 4 r4 <a, fis> 4 r4 <a, fis> 4 | r4 <a, fis> 4 r4 <g, f> 4 r4 <g, f> 4 | }
        \score { #(systemPair mC) }

        mD = { r2 d'8 fis'8 e'8 fis'8 g'4 r4 | g8 bes8 a8 bes8 c'4 r4 c8 ees8 d8 ees8 | fis4 r4 r8 bes'8 a'8 g'8 f'8 ees'8 d'8 c'8 | b8 d'8 cis'8 d'8 e'4 d'4 c'4 b4 | }
        \score { #(systemPair mD) }

        mE = { b8 d'8 cis'8 d'8 e'4 d'4 c'4 b4 | b4 b8 d'8 cis'8 d'8 b4 b8 d'8 cis'8 d'8 | b4 b8 d'8 b4 b8 d'8 e'4 b8 d'8 | b8 d'8 b8 d'8 b8 d'8 b8 d'8 b8 d'8 b8 d'8 | }
        \score { #(systemPair mE) }

        mF = { r2 <g, d b e'> 4 <g, d b e'> 4 r2 | }
        \score { #(systemPair mF) }
