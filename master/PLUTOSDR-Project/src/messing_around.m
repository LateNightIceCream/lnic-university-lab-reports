close all;

receiver = Receiver();
%receiver.init_radio('usb:0');
%receiver.test_blep()


load('C:\Users\st181028\Desktop\PLUTOSDR-Project\src\recordings\rx_capture_2.mat');

% reduce the data for testing
data = data(1500002:end);

rx_filter = comm.RaisedCosineReceiveFilter(...
                        'RolloffFactor', receiver.RolloffFactor, ...
                        'FilterSpanInSymbols', receiver.RaisedCosineFilterSpan, ...
                        'InputSamplesPerSymbol', receiver.SamplesPerSymbol, ...
                        'DecimationFactor', 1);

data = rx_filter(data);
plot(abs(data));
figure()
scatter(real(data), imag(data))

figure()
miniframeo = data(132000:172310);
scatter(real(miniframeo), imag(miniframeo));
scatter(real(data(1:132000)), imag(data(1:132000)));
%plot(abs(data(132000:172310)))

data_bits = qamdemod(data, receiver.ModulationOrder, 'OutputType', 'bit');

figure()
plot(data_bits);

xcorrheader = xcorr(data_bits, receiver.Header');
figure()
plot(xcorrheader);

% header symbols
% => same number of samples as received signal (Fs * Interpolation)


headerSyms = qammod(repmat(receiver.Header, 1, 2)', receiver.ModulationOrder, ...
                    InputType='bit', ...
                    UnitAveragePower=true, ...
                    PlotConstellation=true)
                     
tx_filter = comm.RaisedCosineTransmitFilter( ...
                        'RolloffFactor', receiver.RolloffFactor, ...
                        'FilterSpanInSymbols', receiver.RaisedCosineFilterSpan, ...
                        'OutputSamplesPerSymbol', receiver.SamplesPerSymbol);
          
headerSamps = rx_filter(tx_filter(headerSyms));


headerSamps2 = [headerSamps];

XY = xcorr((data), (headerSamps2));

[M,I] = max(XY)

nonz = find(abs(XY)>1e-14, 1)
XYcrop = XY(nonz:end);
I = I - nonz;

m = zeros(1, length(XYcrop));
m(1,I) = 1;

figure()
sp(1)=subplot(4,1,1);
plot(abs(headerSamps2));
sp(2)=subplot(4,1,2);
plot(abs(data));
sp(3)=subplot(4,1,3);
plot(abs(XYcrop));
sp(4)=subplot(4,1,4);
plot(m);


samples = data;
sps = receiver.SamplesPerSymbol;
mu = 0.2; % initial estimate of phase of sample
out = zeros(length(samples) + 10, 1);
out_rail = zeros(length(samples) + 10, 1); % stores values, each iteration we need the previous 2 values plus current value
i_in = 1; % input samples index
i_out = 3; % output index (let first two outputs be 0)
while i_out < length(samples) && i_in+16 < length(samples)
    out(i_out) = samples(i_in + floor(mu)); % grab what we think is the "best" sample
    %out[i_out] = samples_interpolated[i_in*16 + int(mu*16)]
    out_rail(i_out) = (real(out(i_out)) > 0) + 1i*(imag(out(i_out)) > 0);
    x = (out_rail(i_out) - out_rail(i_out-2)) * conj(out(i_out-1));
    y = (out(i_out) - out(i_out-2)) * conj(out_rail(i_out-1));
    mm_val = real(y - x);
    mu = mu + sps + 0.3*mm_val;
    i_in = i_in + floor(mu); % round down to nearest int since we are using it as an index
    mu = mu - floor(mu); % remove the integer part of mu
    i_out = i_out + 1; % increment output index
end
out = out(3:i_out-1); % remove the first two, and anything after i_out (that was never filled out)
samples = out; % only include this line if you want to connect this code snippet with the Costas Loop later o

figure()
constplot(samples);
%plot(abs(samples));

%figure()
%constplot(mean(samples.^4));

%symbs = qamdemod(data, receiver.ModulationOrder, 'OutputType', 'bit');


function constplot(x)
    scatter(real(x), imag(x));
end
